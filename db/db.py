import sqlite3
import time

seen = 1
pend = 0

#c.execute("DROP TABLE movie_user")

def addMovie(idu, mov, state, conn, c):
    c.execute("SELECT id FROM movie_user WHERE user=? AND movie=?", (str(idu).strip(), str(mov).strip()))
    idm = c.fetchone()
    if(idm==None):
        try:
            with conn:
                c.execute("INSERT INTO movie_user (user, movie, estado) VALUES (?, ?, ?)", (str(idu).strip(), str(mov).strip(), int(state)))
                if(state==1):
                    print('Movie ' + str(mov) + ' added to seen for user ' + str(idu))
                else:
                    print('Movie ' + str(mov) + ' added to pending for user ' + str(idu))
                return 1
        except Exception as e:
            print('Error while adding a row: ' + str(e))
    elif(getState(idu, mov, conn, c)!=state):
        if(state==1):
            setMovie(idu, mov, seen, conn, c)
        elif(state==0):
            setMovie(idu, mov, pend, conn, c)
    else:
        print('This row already exists and could not be added (user=' + str(idu) + ', movie=' + str(mov) + ')')
        return None


def delMovie(idu, mov, conn, c):
    c.execute("SELECT id FROM movie_user WHERE user=? AND movie=?", (str(idu).strip(), str(mov).strip()))
    idm = c.fetchone()
    if(idm!=None):
        try:
            with conn:
                c.execute("DELETE FROM movie_user WHERE user=? AND movie=?", (str(idu).strip(), str(mov).strip()))
                print('Movie added')
                return 1
        except Exception as e:
            print('Error while adding a row: ' + str(e))
    else:
        print('This row does not exists and could not be deleted (user=' + str(idu) + ', movie=' + str(mov) + ')')
        return None


def setMovie(idu, mov, state, conn, c):
    c.execute("SELECT id FROM movie_user WHERE user=? AND movie=?", (str(idu).strip(), str(mov).strip()))
    idm = c.fetchone()
    if(idm!=None):
        if(getState(idu, mov, conn, c)!=state):
            try:
                with conn:
                    c.execute("UPDATE movie_user SET estado=? WHERE id=?", (state, idm[0]))
                    print('Movie state modified')
                    return 1
            except Exception as e:
                print('Error while updating a row: ' + str(e))
        else:
            print('The movie already has this state')
            return 0
    else:
        print('This row does not exists')
        return None

def getMovies(idu, conn, c):
    try:
        c.execute("SELECT movie, estado FROM movie_user WHERE user=?", (str(idu).strip(),))
        movies = c.fetchall()
        mlist = []
        for m in movies:
            mlist.append((m[0], m[1]))
        #print(mlist)
        return mlist
    except Exception as e:
        print('Error retrieving ' + str(idu) + ' list: ' + str(e))

def getState(idu, mov, conn, c):
    c.execute("SELECT id FROM movie_user WHERE user=? AND movie=?", (str(idu).strip(), str(mov).strip()))
    #print((str(idu), str(mov)))
    idm = c.fetchone()
    if(idm!=None):
        try:
            c.execute("SELECT estado FROM movie_user WHERE user=? AND movie=?", (str(idu).strip(), str(mov).strip()))
            estado = c.fetchone()
            return int(estado[0])
        except Exception as e:
            print('Error retrieving seen movies: ' + str(e))
    else:
        #print('This row does not exists')
        return None

def getPendMovies(idu, conn, c):
    try:
        c.execute("SELECT movie FROM movie_user WHERE user={} AND estado={}".format(str(idu), pend))
        movies = c.fetchall()
        mlist = []
        for m in movies:
            mlist.append(m[0])
        print(mlist)
        return mlist
    except Exception as e:
        print('Error retrieving seen movies: ' + str(e))

def getSeenMovies(idu, conn, c):
    try:
        c.execute("SELECT movie FROM movie_user WHERE user={} AND estado={}".format(str(idu), seen))
        movies = c.fetchall()
        mlist = []
        for m in movies:
            mlist.append(m[0])
        print(mlist)
        return mlist
    except Exception as e:
        print('Error retrieving seen movies: ' + str(e))

#addMovie(2323, 126, pend)
#addMovie(2343, 123, pend)
#setMovie(2323, 123, pend)
#setMovie(2326, 123, seen)
#addMovie(2323, 121, seen)
#getMovies(2323)
#getPendMovies(2323)
#getSeenMovies(2323)
