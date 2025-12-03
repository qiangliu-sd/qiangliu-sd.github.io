

from qlMatchNSumUnivs import *


"""Code-STYLE
   modName.py
   ----------
   MY_CONSTANT
   ----------
   funcName(arg_in):
    localVar
   ----------
   MyClass
    _classVar, self.dataVar, self.membFunc
    arg_in, localVar
"""
    
if __name__ == '__main__':
    docFile = 'doc-univ_counts.txt'
    countryFile = 'num-univ-country-2025.txt'
    matchOutFile = 'ql-matched_univs.txt'
    similarThreshold = 88

    print(f"Parsing {docFile}...")
    uDocs = parse_file(docFile, r'^(.*?):\s*([\d\.]+)$')  # Try to match 'Name: score' format

    print(f"Parsing {countryFile}...")
    uCntrs = parse_file(countryFile, r'^([\d\.]+)\s+(.*)')

    if uCntrs is None or uDocs is None:
        sys.exit(1)
        
    uMatches = matchSimilar(uDocs, uCntrs, similarThreshold)
    orderedOutput(uMatches, matchOutFile)

    print(f"Done")
            
