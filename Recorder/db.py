from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
from decouple import config
from sqlalchemy.orm.exc import NoResultFound


class DBWrapper:
    """ """

    def __init__(self):
        engine = create_engine(config('DB_STRING'))  # Connection query
        table_meta = MetaData(engine)
        self.table = Table('settings', table_meta, autoload=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_configuration(self):
        """ Get configuration data from database """
        try:
            setting_obj = self.session.query(self.table).one()
            return {
                'device': setting_obj.device,
                'sampling_rate': setting_obj.sampling_rate,
                'bit_rate': setting_obj.bit_rate,
                'channel': setting_obj.channel,
                'destination': setting_obj.destination,
                'duration': setting_obj.duration,
                'automatic_recording': setting_obj.automate_recording,
                'recording_time': setting_obj.recording_time
            }

        except Exception:
            return None

    def save_configuration(self, **kwargs):
        """ Save configuration data to database """
        pass


if __name__ == '__main__':
    db = DBWrapper()
    db.get_configuration()