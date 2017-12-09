# NOTE: Keeping for the moment until multi-processing job framework is in place
# import datetime
# import logging
# import random
# from time import sleep
# import multiprocessing as mp
#
# import esipy
#
# from api.logging_helper import get_logger
# from api.repos import RegionRepo
#
#
# def hydrate_database():
#     if not _check_regions_populated():
#         _import_regions()
#
#
# def _import_regions():
#     print('import regions')
#     start = datetime.datetime.now()
#     app = esipy.App.create(url='https://esi.tech.ccp.is/latest/swagger.json?'
#                            'datasource=tranquility')
#     headers = {
#         'User-Agent': 'Corp-HQ client '
#                       'https://github.com/fritogotlayed/corp-hq-api and '
#                       'https://github.com/fritogotlayed/corp-hq-ui contact '
#                       '<FritoGotLayed> in game or <Frito> on Tweetfleet.'
#     }  # yapf: disable
#     client = esipy.EsiClient(
#         retry_requests=True, header=headers, raw_body_only=False)
#     end = datetime.datetime.now()
#     # wow... 30 seconds here alone mostly in App.create
#     print('app and client init took %s' % (end - start))
#
#     start = datetime.datetime.now()
#     get_universe_regions = app.op['get_universe_regions']()
#     response = client.request(get_universe_regions)
#
#     region_ids = response.data
#     jobs = []
#     for region_id in region_ids:
#         process = mp.Process(
#             target=_save_eve_region_details, args=(app, client, region_id))
#         process.start()
#         jobs.append(process)
#
#     for j in jobs:  # type: mp.Process
#         j.join()
#     end = datetime.datetime.now()
#     print('region import took %s' % (end - start))
#
#
# def _save_eve_region_details(app, client, region_id):
#     repo = RegionRepo()
#     get_universe_regions_region_id = app.op['get_universe_regions_region_id'](
#         region_id=region_id)
#     tries = 0
#     limit = 3
#     while tries < limit:
#         try:
#             tries += 1
#             response = client.request(get_universe_regions_region_id)
#             region = {
#                 'constellations': response.data['constellations'],
#                 'name': response.data['name'],
#                 'region_id': response.data['region_id']
#             }
#             if 'description' in response.data:
#                 region['description'] = response.data['description']
#             repo.save(region)
#             limit = 0
#         except BaseException as ex:
#             get_logger().warning(ex)
#             sleep(random.randint(tries, tries * 3))
#
#     print(region_id)
#
#
# def _check_regions_populated():
#     repo = RegionRepo()
#     return repo.has_any()
