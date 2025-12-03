
import re
from fuzzywuzzy import process, fuzz

def getConfig():
    """Returns the configuration for the script."""
    return {
        'doc_univ_counts_file': 'doc-univ_counts.txt',
        'num_univ_country_file': 'num-univ-country-2025.txt',
        'output_file': 'matched_universities.txt',
        'similarity_threshold': 88,
        'doc_univ_pattern': r'^(.*?):\s*([\d\.]+)$',
        'num_univ_pattern': r'^([\d\.]+)\s+(.*)',
    }

def parseFile(file_path_in, regex_pattern_in):
    """
    Parses a file and returns a dictionary of names and scores.

    Args:
        file_path_in (str): The path to the file.
        regex_pattern_in (str): The regular expression pattern to parse the file.

    Returns:
        dict: A dictionary with names as keys and scores as values.
    """
    nameScoreDict = {}
    try:
        with open(file_path_in, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(regex_pattern_in, line)

                if match:
                    if match.group(2).isnumeric():
                        name = match.group(1).strip()
                        score = float(match.group(2))
                        nameScoreDict[name] = score
                    else:
                        name = match.group(2).strip()
                        score = float(match.group(1))
                        nameScoreDict[name] = score
    except FileNotFoundError:
        print(f"Error: File not found at {file_path_in}")
        return None
    except Exception as e:
        print(f"Error parsing file {file_path_in}: {e}")
        return None
        
    return nameScoreDict

def parseData(config_in):
    """Parses the data from the input files."""
    print(f"Parsing {config_in['doc_univ_counts_file']}...")
    docUnivs = parseFile(config_in['doc_univ_counts_file'], config_in['doc_univ_pattern'])

    print(f"Parsing {config_in['num_univ_country_file']}...")
    countryUnivs = parseFile(config_in['num_univ_country_file'], config_in['num_univ_pattern'])

    return docUnivs, countryUnivs

def matchUniversities(doc_univs_in, country_univs_in, similarity_threshold_in):
    """Matches universities and returns a list of matches."""
    print("Matching universities between the two files...")
    
    matches = []
    
    # Create a list of choices from the country universities
    choices = list(country_univs_in.keys())
    
    for nameFromDoc, scoreFromDoc in doc_univs_in.items():
        # Find the best match using extractOne, as it's the most direct way for this task
        best_match = process.extractOne(
            nameFromDoc, choices, scorer=fuzz.WRatio, score_cutoff=similarity_threshold_in
        )
        
        if best_match:
            bestMatchName, similarityScore = best_match
            scoreFromCountry = country_univs_in.get(bestMatchName)
            
            if scoreFromCountry is not None:
                totalScore = scoreFromDoc + scoreFromCountry
                matches.append({
                    'univ1_name': nameFromDoc,
                    'univ1_score': scoreFromDoc,
                    'univ2_name': bestMatchName,
                    'univ2_score': scoreFromCountry,
                    'total_score': totalScore,
                    'similarity': similarityScore
                })

    matches.sort(key=lambda x: x['total_score'], reverse=True)
    return matches

def writeResults(matches_in, config_in):
    """Writes the matched results to the output file."""
    outputFile = config_in['output_file']
    print(f"Writing {len(matches_in)} matches to {outputFile}...")
    with open(outputFile, 'w', encoding='utf-8') as f:
        f.write(f"Matches found between '{config_in['doc_univ_counts_file']}' and '{config_in['num_univ_country_file']}'\n")
        f.write("Sorted by the sum of their scores.\n")
        f.write("="*50 + "\n\n")
        
        for match in matches_in:
            f.write(
                f"Total Score: {match['total_score']:.2f} | "
                f"File 1: {match['univ1_name']} ({match['univ1_score']:.2f}) | "
                f"File 2: {match['univ2_name']} ({match['univ2_score']:.2f}) | "
                f"Similarity: {match['similarity']}%\n"
            )
