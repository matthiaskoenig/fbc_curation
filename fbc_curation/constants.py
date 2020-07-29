class CuratorConstants:
    OBJECTIVE_KEY = "objective"
    FVA_KEY = "fva"
    GENE_DELETION_KEY = "gene_deletion"
    REACTION_DELETION_KEY = "reaction_deletion"
    KEYS = [
        OBJECTIVE_KEY,
        FVA_KEY,
        GENE_DELETION_KEY,
        REACTION_DELETION_KEY,
    ]

    # output filenames
    OBJECTIVE_FILENAME = f"01_{OBJECTIVE_KEY}.tsv"
    FVA_FILENAME = f"02_{FVA_KEY}.tsv"
    GENE_DELETION_FILENAME = f"03_{GENE_DELETION_KEY}.tsv"
    REACTION_DELETION_FILENAME = f"04_{REACTION_DELETION_KEY}.tsv"

    NUM_DECIMALS = 6  # decimals to write in the solution

    STATUS_OPTIMAL = "optimal"
    STATUS_INFEASIBLE = "infeasible"
    STATUS_CODES = [STATUS_OPTIMAL, STATUS_INFEASIBLE]

    VALUE_INFEASIBLE = ''

    OBJECTIVE_FIELDS = ["model", "objective", "status", "value"]
    FVA_FIELDS = ["model", "objective", "reaction", "status", "minimum", "maximum"]
    GENE_DELETION_FIELDS = ["model", "objective", "gene", "status", "value"]
    REACTION_DELETION_FIELDS = ["model", "objective", "reaction", "status", "value"]

