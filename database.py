from sqlalchemy import *

def bootstrap_db():
	db = create_engine('sqlite:///phil.cdc.sql')

	db.echo = True
	metadata = MetaData(db)

	phil = Table('phil', metadata,
	    Column('id', Integer, primary_key=True),
	    Column('desc', String),         # Description - Extensive and authoritative explanation of the visual image or video file
	    Column('categories', String),   # Categories - used to describe the image
	    Column('credit', String),       # Photo Credit - Photographer or Videographer who took the photo or shot the video
	    Column('provider', String),      # Content Provider - The contributor of the asset
	    Column('source', String),       # Source Library - Where the image originated
	    Column('path_to_img', String),  # seth: static url to hi-res images
	    Column('is_color', Boolean),    # Color Scheme - Color or Black & White
	    Column('creation', DateTime),   # Creation Date - When the object was created (photo taken, video shot, etc.)
	    Column('upload', DateTime),     # Upload Date - When the image entered the PHIL database
	    Column('access_time', DateTime) # seth: time/day we accessed the content
	)
	metadata.create_all(db)
