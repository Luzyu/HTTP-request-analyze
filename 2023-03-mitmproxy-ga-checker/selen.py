from be_data import (
  url_test_list1 as list1,
  url_test_list2 as list2,
  url_test_list3 as list3,
  be_hostname,
  be_path_list,
)
from tools.functions import (
  url_set_builder,
  visit_all_urls
)


# Build the URL list
# list = url_set_builder(be_hostname, be_path_list)
# list = url_set_builder(be_hostname, list3)
list = list1

# Visit all the URLs
visit_all_urls(list, False, 'proxy-on', 'headless-on')

# Test with going to a single URL
# go_to_url(test_url, False, 'proxy-on', 'headless-off')
