import MySQLdb

class DB:
  """
  Quick and dirty library for MySQL queries.
  """
  
  def __init__(self, user='username', passwd='passwd', db='db', use_unicode=True, charset='utf-8'):
    """Inits the database connections and sets up the cursor"""
    self.db = MySQLdb.connect(user=user, passwd=passwd, db=db, use_unicode=use_unicode, charset=charset)
    self.c = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
  
  def commit(self):
    """Commits queries"""
    self.db.commit()
  
  def close(self):
    """Closes the connection, necessary to commit changes"""
    self.commit()
  
  def q_prepare(self, txt):
    """Pseudo prepare for quick and dirty queries"""
    txt = unicode(txt)
    txt = txt.replace('"', '\\"')
    return txt
  
  def q(self, query):
    """Runs a select type query and returns the results"""
    self.c.execute(query)
    data = self.c.fetchall()
    self.commit()
    return data
  
  def nq(self, query):
    """Runs an update, insert or delete query silently"""
    self.c.execute(query)
    self.commit()
  
  def iq(self, table, obj):
    """Insert query
    table: the table name
    obj: a dict describing the object to insert, example: {'name':name, 'url':url}
    """
    fields = []
    values = []
    
    for k in obj:
      fields.append(k)
      values.append('"' + self.q_prepare(obj[k]) + '"')
    
    query = """INSERT INTO %(table)s (%(fields)s) VALUES (%(values)s)""" % {'table':table, 'fields':','.join(fields), 'values':','.join(values)}
    self.nq(query)

  def uq(self, table, obj, id, id_name = "id"):
    """Update query
    table: the table name
    obj: a dict describing the object to update, example: {'name':name, 'url':url}
    id: the object id
    id_name: the name of the id field
    """
    values = []

    for k in obj:
      values.append("%(key)s = \"%(value)s\"" % {'key':k, 'value':self.q_prepare(obj[k])})

    query = """UPDATE %(table)s SET %(values)s WHERE %(id_name)s = '%(id)s'""" % {'table':table, 'values':','.join(values), 'id_name':id_name, 'id':str(id)}
    self.nq(query)
  
  def dq(self, table, id, id_name = "id"):
    """Delete query
    table: the table name
    id: the object id
    id_name: the name of the id field
    """
    query = """DELETE FROM %(table)s WHERE %(id_name)s = '%(id)s'""" % {'table':table, 'id_name':id_name, 'id':str(id)}
    self.nq(query)

  def dqw(self, table, where):
    """Delete where query
    table: the table name
    where: the where part of the query, example: "points >= 30"
    """
    query = """DELETE FROM %(table)s WHERE %(where)s""" % {'table':table, 'where':where}
    self.nq(query)

  def sq(self, table, id, id_name = "id", fields='*'):
    """Select query
    table: the table name
    id: ID of the object
    id_name: name of the id field
    fields: fields if necessary, example: "id, name"
    """
    query = """SELECT %(fields)s FROM %(table)s WHERE %(id_name)s = '%(id)s'""" % {'fields': fields, 'table':table, 'id_name':id_name, 'id':str(id)}
    results = self.q(query)
    return results

  def sqf(self, table, id_name="id"):
    """Select first query
    table: the table name
    """
    query = """SELECT * FROM %(table)s WHERE 1 ORDER BY %(id_name)s ASC LIMIT 1""" % {'table':table, 'id_name':id_name}
    results = self.q(query)
    return results

  def sql(self, table, id_name="id"):
    """Select last query
    table: the table name
    """
    query = """SELECT * FROM %(table)s WHERE 1 ORDER BY %(id_name)s DESC LIMIT 1""" % {'table':table, 'id_name':id_name}
    results = self.q(query)
    return results

  def sqw(self, table, where, order="", group="", limit="", fields='*'):
    """Select where query
    table: the table name
    where: the where part of the query, example: "points >= 30"
    order: order statement if necessary, example: "id DESC"
    group: group by statement if necessary, example: "name"
    limit: limit statement if necessary, example: "0, 5"
    fields: fields if necessary, example: "id, name"
    """
    query = """SELECT %(fields)s FROM %(table)s WHERE %(where)s""" % {'fields':fields, 'table':table, 'where':where}
    
    if(order != ""):
      query += " ORDER BY %s" % (order)
    
    if(group != ""):
      query += " GROUP BY %s" % (group)
    
    if(limit != ""):
      query += " LIMIT %s" % (limit)
    
    results = self.q(query)
    return results
