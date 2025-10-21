from __future__ import absolute_import, print_function, division

import logging
from collections import OrderedDict

import numpy
import pandas
from cobra import Reaction
from cobra.util import fix_objective_as_constraint

from optlang.interface import UNBOUNDED, OPTIMAL
from optlang.symbolics import Zero

logger = logging.getLogger(__name__)


def flux_variability_analysis(model, reactions=None, fraction_of_optimum=0.0):
    """Flux variability analysis.

    Parameters
    ----------
    model : cobra.Model
    reactions: None or iterable
        The list of reaction whose lower and upper bounds should be determined.
        If `None`, all reactions in `model` will be assessed.
    fraction_of_optimum : float
        Fix the objective of the model to a fraction of it's max. Expected to be within [0;1]. Lower values increase
        variability.

    Returns
    -------
    FluxVariabilityResult
        FluxVariabilityResult with DataFrame data_frame property containing the results of the flux variability
        analysis.

    """
    if reactions is None:
        reactions = model.reactions
    else:
        reactions = model.reactions.get_by_any(reactions)
    fva_sol = OrderedDict()
    lb_flags = dict()
    with model:
        if fraction_of_optimum > 0.0:
            fix_objective_as_constraint(model, fraction=fraction_of_optimum)
        model.objective = Zero

        model.objective.direction = "min"
        for reaction in reactions:
            lb_flags[reaction.id] = False
            fva_sol[reaction.id] = dict()
            model.solver.objective.set_linear_coefficients(
                {reaction.forward_variable: 1.0, reaction.reverse_variable: -1.0}
            )
            model.solver.optimize()
            if model.solver.status == OPTIMAL:
                fva_sol[reaction.id]["lower_bound"] = model.objective.value
            elif model.solver.status == UNBOUNDED:
                fva_sol[reaction.id]["lower_bound"] = -numpy.inf
            else:
                lb_flags[reaction.id] = True
            model.solver.objective.set_linear_coefficients(
                {reaction.forward_variable: 0.0, reaction.reverse_variable: 0.0}
            )

            assert model.objective.expression == 0, model.objective.expression

        model.objective.direction = "max"
        for reaction in reactions:
            ub_flag = False
            model.solver.objective.set_linear_coefficients(
                {reaction.forward_variable: 1.0, reaction.reverse_variable: -1.0}
            )

            model.solver.optimize()
            if model.solver.status == OPTIMAL:
                fva_sol[reaction.id]["upper_bound"] = model.objective.value
            elif model.solver.status == UNBOUNDED:
                fva_sol[reaction.id]["upper_bound"] = numpy.inf
            else:
                ub_flag = True

            if lb_flags[reaction.id] is True and ub_flag is True:
                fva_sol[reaction.id]["lower_bound"] = 0
                fva_sol[reaction.id]["upper_bound"] = 0
                [lb_flags[reaction.id], ub_flag] = [False, False]
            elif lb_flags[reaction.id] is True and ub_flag is False:
                fva_sol[reaction.id]["lower_bound"] = fva_sol[reaction.id][
                    "upper_bound"
                ]
                lb_flags[reaction.id] = False
            elif lb_flags[reaction.id] is False and ub_flag is True:
                fva_sol[reaction.id]["upper_bound"] = fva_sol[reaction.id][
                    "lower_bound"
                ]
                ub_flag = False

            model.solver.objective.set_linear_coefficients(
                {reaction.forward_variable: 0.0, reaction.reverse_variable: 0.0}
            )

            assert model.objective.expression == 0, model.objective.expression

            assert lb_flags[reaction.id] is False and ub_flag is False, (
                "Something is wrong with FVA (%s)" % reaction.id
            )

    df = pandas.DataFrame.from_dict(fva_sol, orient="index")
    lb_higher_ub = df[df.lower_bound > df.upper_bound]
    # this is an alternative solution to what I did above with flags
    # Assert that these cases really only numerical artifacts
    try:
        assert ((lb_higher_ub.lower_bound - lb_higher_ub.upper_bound) < 1e-6).all()
    except AssertionError:
        logger.debug(
            list(
                zip(
                    model.reactions,
                    (lb_higher_ub.lower_bound - lb_higher_ub.upper_bound) < 1e-6,
                )
            )
        )
    df.lower_bound[lb_higher_ub.index] = df.upper_bound[lb_higher_ub.index]

    return FluxVariabilityResult(df)


class FluxVariabilityResult:
    def __init__(self, data_frame, *args, **kwargs):
        self._data_frame = data_frame

    @property
    def data_frame(self):
        return self._data_frame

    def __getitem__(self, item):
        return self._data_frame[item]

    def upper_bound(self, item):
        if isinstance(item, Reaction):
            item = item.id
        return self["upper_bound"][item]

    def lower_bound(self, item):
        if isinstance(item, Reaction):
            item = item.id
        return self["lower_bound"][item]

    def iterrows(self):
        return self._data_frame.iterrows()
