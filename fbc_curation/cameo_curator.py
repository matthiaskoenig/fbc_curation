
import logging
import pandas as pd
from cobra.core import Reaction, Gene, Model
from cameo import load_model, fba

from fbc_curation.fbc_curator import FBCCuratorImplementation, FBCCuratorResult

logger = logging.getLogger(__name__)


class FBCCuratorCameo(FBCCuratorImplementation):
    """ FBC curator based on cameo.

    Cameo is a high-level python library developed to aid the strain design
    process in metabolic engineering projects. The library provides a modular
    framework of simulation and strain design methods that targets developers
    that want to develop new design algorithms and custom analysis workflows.
    Furthermore, it exposes a high-level API to users that just want to
    compute promising strain designs.

    https://pythonhosted.org/cameo/
    """

    def __init__(self, model_path):
        super(FBCCuratorCameo, self).__init__(model_path=model_path)

    def read_model(self):
        self.model = load_model(str(self.model_path))  # type: cobra.core.Model

    def objective(self) -> pd.DataFrame:

        try:
            # fbc optimization
            result = fba(self.model)
            value = result.objective_value
            status = FBCCuratorResult.STATUS_OPTIMAL
        except Exception as e:
            logger.error(f"{e}")
            value = ''
            status = FBCCuratorResult.STATUS_INFEASIBLE

        return pd.DataFrame(
            {
                "model": model.id,
                "objective": [self.objective_id],
                "status": [status],
                "value": [value],
             })



# 02 FVA
from cameo.flux_analysis.analysis import flux_variability_analysis, FluxVariabilityResult
result_fva = flux_variability_analysis(model)  # type: FluxVariabilityResult
print(result_fva.data_frame)

# 03 Gene deletions
gene = model.genes.b0351  # type: cobra.core.Gene
print(gene)
gene.knock_out()
for reaction in gene.reactions:
    if not reaction.functional:
        reaction.bounds = (0, 0)



# 04 Reaction deletions
reaction = model.reactions.PGK  # type: cobra.core.Reaction
reaction.bounds = (0, 0)


print(reaction, reaction.lower_bound, reaction.upper_bound)
result2 = fba(model)
print(result2)




