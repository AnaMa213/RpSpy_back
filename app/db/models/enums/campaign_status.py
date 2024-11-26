import enum


class CampaignStatus(str, enum.Enum):
    IN_PROGRESS = "en_cours"
    COMPLETED = "terminee"
    ARCHIVED = "archivee"
