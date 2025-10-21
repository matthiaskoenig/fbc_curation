import logging
import pandas
import sympy
from cobra import Reaction
from optlang.interface import OptimizationExpression
from sympy.parsing.sympy_parser import parse_expr


__all__ = ["fba"]

logger = logging.getLogger(__name__)


def fba(model, objective=None, reactions=None):
    """Flux Balance Analysis.

    Parameters
    ----------
    model: cobra.Model
    objective: a valid objective - see SolverBaseModel.objective (optional)

    Returns
    -------
    FluxDistributionResult
        Contains the result of the linear solver.

    """
    with model:
        if objective is not None:
            model.objective = objective
        solution = model.optimize(raise_error=True)
        if reactions is not None:
            result = FluxDistributionResult(
                {r: solution[r] for r in reactions}, solution.objective_value
            )
        else:
            result = FluxDistributionResult.from_solution(solution)
        return result


class FluxDistributionResult:
    """Contains a flux distribution of a simulation method."""

    @classmethod
    def from_solution(cls, solution, *args, **kwargs):
        return cls(solution.fluxes, solution.objective_value, *args, **kwargs)

    def __init__(self, fluxes, objective_value, *args, **kwargs):
        self._fluxes = fluxes
        self._objective_value = objective_value

    def __getitem__(self, item):
        if isinstance(item, Reaction):
            return self.fluxes[item.id]
        elif isinstance(item, str):
            try:
                return self.fluxes[item]
            except KeyError:
                exp = parse_expr(item)
        elif isinstance(item, OptimizationExpression):
            exp = item.expression
        elif isinstance(item, sympy.Expr):
            exp = item
        else:
            raise KeyError(item)

        return exp.evalf(subs={v: self.fluxes[v.name] for v in exp.atoms(sympy.Symbol)})

    @property
    def data_frame(self):
        return pandas.DataFrame(
            list(self._fluxes.values), index=list(self._fluxes.keys()), columns=["flux"]
        )

    @property
    def fluxes(self):
        return self._fluxes

    @property
    def objective_value(self):
        return self._objective_value

    def iteritems(self):
        # TODO: I don't think this is needed anymore
        return self.fluxes.items()

    def items(self):
        return self.fluxes.items()

    def keys(self):
        return self.fluxes.keys()

    def values(self):
        return self.fluxes.values()
