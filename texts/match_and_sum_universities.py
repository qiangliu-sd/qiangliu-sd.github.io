import subprocess
import sys
import re


try:
    from fuzzywuzzy import fuzz, process
except ImportError:
    print("fuzzywuzzy library not found. Trying to install it...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fuzzywuzzy[speedup]"])
        from fuzzywuzzy import fuzz, process
        print("fuzzywuzzy installed successfully.")
    except Exception as e:
        print(f"Failed to install fuzzywuzzy: {e}")
        print("Please install it manually: pip install fuzzywuzzy[speedup]")
        sys.exit(1)

def parse_file(filepath):
    """Parses a university file, returning a list of (score, name) tuples."""
    universities = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Try to match 'Name: score' format
                match1 = re.match(r'^(.*?):\s*([\d\.]+)$', line)
                # Try to match 'score Name' format
                match2 = re.match(r'^([\d\.]+)\s+(.*)', line)

                if match1:
                    score = float(match1.group(2))
                    name = match1.group(1).strip()
                    universities.append({'score': score, 'name': name})
                elif match2:
                    score = float(match2.group(1))
                    name = match2.group(2).strip()
                    universities.append({'score': score, 'name': name})
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error parsing file {filepath}: {e}")
        return None
        
    return universities

def normalize_name(name):
    """Normalizes a university name for better matching."""
    name = re.sub(r'\(.*?\)', '', name).lower()
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip()


# --- Main script ---

file1 = 'doc-univ_counts.txt'
file2 = 'num-univ-country-2025.txt'
output_file = 'matched_universities.txt'

# 1. Parse both files
print(f"Parsing {file1}...")
univs1 = parse_file(file1)

print(f"Parsing {file2}...")
univs2 = parse_file(file2)

if univs1 is None or univs2 is None:
    sys.exit(1)
    
# Create a list of names for matching
choices = [u['name'] for u in univs2]

# 2. Match universities and sum scores
print("Matching universities between the two files...")
matches = []
similarity_threshold = 85

matched_from_file2 = set()

for univ1 in univs1:
    best_match_name, score = process.extractOne(univ1['name'], choices, scorer=fuzz.WRatio)
    
    if score >= similarity_threshold:
        univ2 = next((u for u in univs2 if u['name'] == best_match_name), None)

        if univ2 and univ2['name'] not in matched_from_file2:
            total_score = univ1['score'] + univ2['score']
            matches.append({
                'univ1_name': univ1['name'],
                'univ1_score': univ1['score'],
                'univ2_name': univ2['name'],
                'univ2_score': univ2['score'],
                'total_score': total_score,
                'similarity': score
            })
            matched_from_file2.add(univ2['name'])

# 3. Sort the matches
matches.sort(key=lambda x: x['total_score'], reverse=True)

# 4. Write to output file
print(f"Writing {len(matches)} matches to {output_file}...")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Matches found between '{file1}' and '{file2}'\n")
    f.write("Sorted by the sum of their scores.\n")
    f.write("="*50 + "\n\n")
    
    for match in matches:
        f.write(f"Total Score: {match['total_score']:.2f} | File 1: {match['univ1_name']} ({match['univ1_score']:.2f}) | File 2: {match['univ2_name']} ({match['univ2_score']:.2f}) (Similarity: {match['similarity']}%)\n")

print(f"Done.")
