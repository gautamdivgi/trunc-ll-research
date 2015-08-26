from acctutil import acct_util
from rpytools.util import write_data

def main():
	cats = [None, 'catm\n', 'catd\n', 'cath\n']

	for cat in cats:
		r = acct_util(cat)

		tuf_pfx = "tu_g."
		duf_pfx = "du_g."

		sfx = "all"

		tu = r[1]
		du = r[2]

		if cat != None:
			sfx = cat.strip()
		
		tuf = tuf_pfx + sfx
		duf = duf_pfx + sfx

		write_data(tuf, tu)
		write_data(duf, du)

if __name__ == "__main__":
	main()
