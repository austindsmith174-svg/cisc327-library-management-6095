import services
import os
from database import init_database, add_sample_data


if os.path.exists('library.db'): os.remove('library.db')
init_database()
add_sample_data()