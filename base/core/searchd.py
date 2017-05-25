# encoding=utf-8
import os, sys
import time, datetime

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../', "apps")))

#from django.core.management import setup_environ
from django.conf import settings
#setup_environ(settings)


from redis_model.queue import Client
from spx.sphinxapi import *
from django.db import connections
conn = connections['sphinx']


#sphinx settings
import logging
cl = SphinxClient()
host = settings.SPHINXES["host"]
port = settings.SPHINXES["port"]

cl.SetServer(host, port)
cl._maxmatches = settings.SPHINXES["maxmatches"]

class SphinxSearch(object):
	def search(self, query, **kwargs):
		"""
		 search from index
		 params : mode ,SPH_MATCH_ALL ......
		"""
		#reset reqs
		cl._reqs = []
		mode = kwargs.get("mode", SPH_MATCH_ALL)
		cl.SetMatchMode(mode)

		#set filter
		filtervals = kwargs.get("filtervals")
		filtercol = kwargs.get("filtercol")
		if filtervals and filtercol:
			cl.SetFilter(filtercol, filtervals)

		#set group by
		groupby = kwargs.get("groupby")
		groupsort = kwargs.get("groupsort")
		if groupby:
			cl.SetGroupBy(groupby, SPH_GROUPBY_ATTR, groupsort)

		#set sort by
		sortby = kwargs.get("sortby")
		if sortby:
			cl.SetSortMode(SPH_SORT_EXTENDED, sortby)

		offset = kwargs.get("offset", 0)
		limit = kwargs.get("limit")
		if limit:
			cl.SetLimits(offset, limit, max(limit, cl._maxmatches))
			
		indexer = kwargs.get("indexer", "user_index,delta_user_index,update_user_index")
		index = kwargs.get("index", indexer)
		res = cl.Query(query, index)

		if not res:
			print 'query failed: %s' % cl.GetLastError()
		return res


	def unpack(self, data):
		ids = []
		if data:
			matches = data.get("matches")
			for m in matches:
				mid = m.get('id')
				if mid:
					ids.append(str(mid))
			return ids
		else:
			print "no matchs"

	def get_from_db(self, sql):
		try:
			cursor = conn.cursor()
			cursor.execute(sql)
			rows = cursor.fetchall()
			cursor.close()
			return rows
		except Exception, e:
			try:
				cursor.close()
			except Exception:
				pass
			logging.error( "Error %d: %s" % (e.args[0], e.args[1]) )


class UserSearch(SphinxSearch):
	def search(self, query, start_count=0, page_count=20, **kwargs):
		kwargs["limit"] = page_count
		kwargs["offset"] = start_count
		kwargs["indexer"] = "user_index,delta_user_index,update_user_index"
		data = super(UserSearch, self).search(query, **kwargs)
		if not data:
			return [],0
		
		total_found = data["total_found"]
		ids = self.unpack(data)
		if ids:
			rows = self.get_user_from_db(ids, page_count, start_count)
			data_ids = []
			if rows:
				for row in rows:
					data_ids.append(row[0])

			return data_ids, total_found
		else:
			return [],0

	def get_user_from_db(self, ids, limit, offset):
		if ids:
			sid = ",".join(ids)
			if len(ids) > 1:
				sql = "select mongo_id from users where id in (%s) order by FIELD(%s)" % (sid, sid)
			else:
				sql = "select mongo_id from users where id in (%s)" % sid
			return self.get_from_db(sql)


class PostSearch(SphinxSearch):
	def search(self, query, start_count=0, page_count=20, **kwargs):
		kwargs["limit"] = page_count
		kwargs["offset"] = start_count
		kwargs["indexer"] = "posts_index,update_posts_index"
		#kwargs["mode"] = SPH_MATCH_PHRASE
		data = super(PostSearch, self).search(query, **kwargs)
		total_found = data["total_found"]
		ids = self.unpack(data)
		if ids:
			rows = self.get_post_from_db(ids, page_count, start_count)
			data_ids = []
			if rows:
				for row in rows:
					data_ids.append(row[0])
			return data_ids, total_found
		else:
			return [],0

	def get_post_from_db(self, ids, limit, offset):
		if ids:
			sid = ",".join(ids)
			if len(ids) > 1:
				sql = "select mongo_id from posts where id in (%s) order by FIELD(%s)" % (sid, sid)
			else:
				sql = "select mongo_id from posts where id in (%s)" % sid
			return self.get_from_db(sql)


def main():
	print "[user search]"
	us = UserSearch()
	rows, total_count = us.search("rt111")
	print total_count, rows

	print "[post search]"
	us = PostSearch()
	rows, total_count = us.search("y")
	print total_count, rows


if __name__ == "__main__":
	main()
