from os import chdir as cd
import glob
from string import punctuation


def load_files(pathin, extension='.cha'):
    """This function loads the raw contents of all files in the given directory
    with the given extension and returns it as a sorted list."""
    
    cd(pathin)  # change working directory to the data folder

    file_contents = []  # make empty list to store raw file contents

    # loop over all files in the folder with the .cha extension
    # sorted() is needed here; otherwise, the files will be in a random order
    for file in sorted(glob.glob('*' + extension)):
        with open(file,'r', encoding='utf-8') as f:  
            text = f.read()  # read in the contents of the file ...
            file_contents.append(text)  # ... and append it to a list
            
    return file_contents


def clean_transcript(raw_transcript):
    """Clean a raw transcript given as a string and return it as a list of
    utterances as tuples with the format (speaker, utterance)."""
    
    lines = raw_transcript.split('\n')  # split the content into lines
    utterance_lines = []  # prepare a list for cleaned utterance lines
    
    for line in lines:  # run over each line one by one to clean
        if line.startswith('*'):  # but only if it's an actual utterance line
                                  # (and not metadata or grammar line)
            
            speaker = line[1:4]  
            utterance = line.split('\t')[1]  # ()'\t' = tab character)
            
            # since the utterance lines also contains punctuation, clean it
            cleaned_utterance = ''  # prepare empty string for clean utterance
            for char in utterance:  # loop over each character in the string
                if char not in punctuation:  # test if it's punctuation
                    cleaned_utterance += char  # if not, add it
            # remove superfluous spaces
            cleaned_utterance = ' '.join(cleaned_utterance.split()) 
            
            # store each line as a tuple where [0] is the speaker and
            # [1] the actual utterance
            utterance_line = (speaker, cleaned_utterance)
            utterance_lines.append(utterance_line)
    
    return utterance_lines


def calculate_mlu(transcript, speaker):
    """Calculate word MLU in a transcript for the given speaker."""
    
    mlus = []  # prepare a list to store MLU measures in

    speaker_utterances = []  # prepare a list for the speaker's utterances
    for line in transcript:
        if line[0] == speaker:
            speaker_utterances.append(line[1])

    tokens = []  # prepare a list for tokens
    for utterance in speaker_utterances:  # lopp over each utterance
        tokens += utterance.split()  # split it into tokens and add it

    ## calculate MLU: number of words / number of utterances
    mlu = len(tokens) / len(speaker_utterances)
    
    return mlu


def get_childs_age(raw_transcript):
    """Get the Target Child's age from a raw transcript."""
    
    child_id_line = None
    for line in raw_transcript.split('\n'):
        if line.startswith('@ID') and 'Target_Child' in line:
            child_id_line = line
            break  # the right line is found; move on

    if not child_id_line:
        print('WARNING: Child ID line not found; age not retrieved!')
        return None
            
    # break the line into "info" chunks
    participant_raw = child_id_line.split('\t')[1]
    info = participant_raw.split('|')
    
    # the age is given as YEARS;MONTHS.DAYS, e.g. 2;03.08
    # get this as a raw string. Convert the values to int along the way
    age_raw = info[3]
    years_monthsdays = age_raw.split(';')  # [YEARS, MONTHS+DAYS]
    years = int(years_monthsdays[0])  # first item is years
    months_days = years_monthsdays[1].split('.')  # [MONTHS, DAYS]
    months = int(months_days[0])  # first item is months
    try:  # sometimes, days are not given;
          # hence, we prepare for an exception
        days = int(months_days[1])  # second item is days
    except:  # if something goes wrong in the parsing, just write 0
        days = 0
    # calculate total number of days (month = 30 days, for simplicity)
    days_total = years * 365 + months * 30 + days
    # then calculate years based on the number of days
    normalized_years = days_total / 365
    
    return normalized_years
