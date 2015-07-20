from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
import uuid

# Initialise SQLAlchemy extention
db = SQLAlchemy()

# Store the UUID of items as per the csv file
# this utility method has been provided by
# the SQLAlchemy documentation 
class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if isinstance(value, list):
                result = []
                for val in value:
                    if not isinstance(val, uuid.UUID):
                        result.append("%.32x" % uuid.UUID(val))
                    else:
                        # hexstring
                        result.append("%.32x" % val)
                return ','.join(result)

            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
