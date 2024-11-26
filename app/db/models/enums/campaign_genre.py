import enum


class CampaignGenre(str, enum.Enum):
    FANTASY = "fantastique"
    SCI_FI = "science-fiction"
    HORROR = "horreur"
    POST_APO = "post-apocalyptique"
    CHTULHU = "chtulhu"
    AUTRE = "autre"
