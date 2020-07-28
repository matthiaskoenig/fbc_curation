class CuratorConstants:
    KEYS = ["objective", "fva", "gene_deletion", "reaction_deletion"]

    # default output filenames
    FILENAME_OBJECTIVE_FILE = "01_objective.tsv"
    FILENAME_FVA_FILE = "02_fva.tsv"
    FILENAME_GENE_DELETION_FILE = "03_gene_deletion.tsv"
    FILENAME_REACTION_DELETION_FILE = "04_reaction_deletion.tsv"

    NUM_DECIMALS = 6  # decimals to write in the solution

    STATUS_OPTIMAL = "optimal"
    STATUS_INFEASIBLE = "infeasible"
    VALUE_INFEASIBLE = ''

    OBJECTIVE_VALUE_COLUMNS = ["model", "objective", "status", "value"]
    FVA_COLUMNS = ["model", "objective", "reaction", "status", "minimum", "maximum"]
    GENE_DELETIONS_COLUMNS = ["model", "objective", "gene", "status", "value"]
    REACTION_DELETION_COLUMNS = ["model", "objective", "reaction", "status", "value"]

