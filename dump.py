# Required for rest of hug scripts
from bitshares import BitShares
from bitshares.account import Account
from bitshares.instance import set_shared_bitshares_instance # Used to reduce bitshares instance load
import bitshares
import sys
import ujson # For outputting to disk
from progressbar import Bar, ETA, ProgressBar, Percentage # For providing progressbar functionality. This is actually "progressbar33" in python3.

"""
Configure Full/API node for querying network info
Only enable ONE of the following API nodes!
"""
full_node_url = 'wss://bitshares.openledger.info/ws' # Berlin, Germany. Telegram: @xeroc
#full_node_url = 'wss://singapore.bitshares.apasia.tech/ws', # Singapore. Telegram: @murda_ra
#full_node_url = 'wss://japan.bitshares.apasia.tech/ws', # Tokyo, Japan. Telegram: @murda_ra
#full_node_url = 'wss://seattle.bitshares.apasia.tech/ws', # Seattle, WA, USA. Telegram: @murda_ra
#full_node_url = 'wss://us-ny.bitshares.apasia.tech/ws', # New York, NY, USA. Telegram: @murda_ra
#full_node_url = 'wss://bitshares.apasia.tech/ws', # Bangkok, Thailand. Telegram: @murda_ra
#full_node_url = 'wss://slovenia.bitshares.apasia.tech/ws', # Slovenia. Telegram: @murda_ra
#full_node_url = 'wss://openledger.hk/ws', # Hone Kong. Telegram: @ronnyb
#full_node_url = 'wss://dex.rnglab.org", # Netherlands. Telegram: @naueh
#full_node_url = 'wss://bitshares.crypto.fans/ws', # https://crypto.fans/ Telegram: @startail
#full_node_url = 'wss://eu.openledger.info/ws', # Nuremberg, Germany. Telegram: @xeroc
bitshares_full_node = BitShares(full_node_url, nobroadcast=False)
set_shared_bitshares_instance(bitshares_full_node)
# End of node configuration

def write_json_to_disk(json_data, start, end):
	"""
	When called, write the json_data to a json file.
	We will end up with many vote_data_*_*.json files.
	These files will be merged using jq.
	"""
	filename = "vote_data_" + start + "_" + end
	with open(filename, 'w') as outfile:
		ujson.dump(json_data, outfile, encode_html_chars=False, escape_forward_slashes=False, ensure_ascii=False) #Write JSON to data.json (disk)

def dump_vote_tx(start, end):
	"""Enable retrieving and displaying any BTS object in JSON."""
	vote = {}
	vote['votes'] = []

	widgets = [Percentage(), # Setting how we wan the progress bar to look
			   ' ', Bar(),
			   ' ', ETA()]

	input_range = end - start
	scrape_range_ref = input_range + 1
	pbar = ProgressBar(widgets=widgets, maxval=scrape_range_ref).start() #Prepare the progress bar
	progress_iterator = 0

	for x in range(start, end):
		pbar.update(progress_iterator + 1) # Display incremented progress
		progress_iterator += 1 # Iterate the progress bar for next iteration

		object_id = "1.11." + str(x)
		try:
			retrieved_object = bitshares_full_node.rpc.get_objects([object_id])[0]
		except:
			continue

		if retrieved_object is not None:
			if 'new_options' in retrieved_object.keys():
				# Log details!
				print("Vote!")
				vote['votes'].append(retrieved_object)
			#else:
				#print("Not a vote!")
	return vote

if __name__ == '__main__':
	scrape_start = int(sys.argv[1]) # Scrape tx from
	scrape_stop = int(sys.argv[2]) # Scrape tx to
	if (scrape_start < scrape_stop and scrape_start >= 0):
		dumped_vote_data = dump_vote_tx(scrape_start, scrape_stop) # Extract account update tx
		write_json_to_disk(dumped_vote_data, scrape_start, scrape_stop) # outputs into file 'vote_data.json'
	else:
		print("Input valid input data.")
