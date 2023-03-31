from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def keys(cls):
        return [k.name for k in cls]

    @classmethod
    def values(cls):
        return [k.value for k in cls]

    @classmethod
    def items(cls):
        return [(k.value, k.name) for k in cls]


class TypePublishEnumEnum(BaseEnum): 
        ARTICLE = "ARTICLE"
        ACTUALITE = "ACTUALITE"
        DECRET =  "DECRET"
        DROITS = "DROITS"
        RESOLUTION = "RESOLUTION"
        INFORMATION = "INFORMATION"
    
    
class StatutDenoEnum(BaseEnum): 
    PENDING = "EN ATTENTE"
    IN_PROGESS = "EN COURS"
    REJECTED = "REJETTEE"
    COMPLETED = "TERMINEE"

class PriorityDenoEnum(BaseEnum): 
    IN_PROGESS = "EN COURS"
    PASSED = "DEJA PASSEE"
   

class NotificationTypeEnum(BaseEnum): 
    EMAIL = "EMAIL"
    SMS = "SMS"
   

class TypeAdminEnum(BaseEnum): 
    SUPERADMIN = "SUPERADMIN"
    TEAMADMIN = "TEAMADMIN"
  
class ActorCategoryEnum(BaseEnum): 
    VICTIM = "VICTIME"
    ACTOR = "ACTEUR"
    WITNESS = "WITNESS"


class VictimTypeEnum(BaseEnum): 
    INDIVIDU = "INDIVIDU"
    GROUP = "GROUPE"
 

class EtapeStatutEnum(BaseEnum): 
    PENDING = "EN ATTENTE"
    IN_PROGESS = "EN COURS"
    COMPLETED = "TERMINEE"