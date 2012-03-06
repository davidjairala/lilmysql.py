Quick and dirty library for MySQL queries.

**Requires MySQLdb library**

    pip install MySQLdb

Ussage is pretty simple and easy:

    from lilmysql import *
    
    db = DB(user='test_user', passwd='password', db='test_db')
    
    # INSERT QUERY
    # Insert into table users username = 'test_user', email = 'email@test.com'
    db.iq('users', {
      'username': 'test_user',
      'email': 'email@test.com',
    })
    
    # UPDATE QUERY
    # Update users table, set username = 'test_user_edited' where id = 2
    db.uq('users', {
      'username': 'test_user_edited',
    }, 2)
    
    # DELETE QUERY - SIMPLE
    # Delete from users table where id = 2
    db.dq('users', 2)
    
    # DELETE QUERY with WHERE CLAUSE
    # Delete from table users where id >= 2
    db.dqw('users', 'id >= %d' % (2))
    
    # SELECT QUERY
    # Select from users table where id = 2
    user = db.sq('users', 2)
    
    # SELECT QUERY FIRST
    # Select first user from users table
    user = dbf.sq('users')
    
    # SELECT QUERY LAST
    # Select last user from users table
    user = dbl.sq('users')
    
    # SELECT QUERY with WHERE CLAUSE
    # Select from users table where id >= 2
    users = db.sqw('users', 'id >= %d' % (2))
    
    db.close()

Some methods include **order**, **group**, **limit** and **fields** parameters where they make sense, be sure to check out each functions' comments.

The whole idea is to reduce the typing done in a project where you need to have direct access to the database and/or don't with to incurr in the added cost of adding an ORM.