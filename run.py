import sys, os

# use local db, when calling: python run.py local-db
# in other case environment variable DATABASE_URL must be settled up
if sys.argv[1:]:
    os.environ.setdefault('DATABASE_URL', 'mysql+pymysql://root:r04sst@localhost/ROASST')

print("We're using DATABASE_URL=", os.environ['DATABASE_URL'])

from roasst.index_page import app
server = app.server

if __name__ == '__main__':

    app.run_server(debug=True)
