import PyPDF2, re

def GetTranscriptText(transcriptFilePath: str) -> str:
    pdfFileObj = open(transcriptFilePath, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    transcriptContents: str = ""
    numPages = pdfReader.numPages
    for i in range(numPages):
        page = pdfReader.getPage(i)
        transcriptContents += page.extractText()
    pdfFileObj.close()
    return transcriptContents

def ValidateTranscript(transcriptFilePath: str = "", transcriptContents: str = None) -> bool:
    # Check if the transcript is a CSULB transcript
    if transcriptContents == None:
        transcriptContents = GetTranscriptText(transcriptFilePath)
    return bool(re.search("California State University, Long Beach . Unofficial Transcript", transcriptContents))
    
def GetClassList (transcriptFilePath: str) -> str:
    # Get pdf contents
    transcriptContents = GetTranscriptText(transcriptFilePath)
    if not ValidateTranscript(transcriptContents = transcriptContents):
        return None

    # To Do: Get Student Name
    # To Do: Get Student ID
    # To Do: Check for Repeated Classes
    # To Do: Read semester season/year
    # To Do: Read test credits given

    regexPatternTransferInstitution = re.compile("Transfer Credit from ([\w ]+)")
    # To Do: Fix this fragile regex pattern:
    regexPatternCourse = re.compile(
    "(?P<repeated>Repeated)?.*\n"
    "(?P<department>[A-Z ]+ +)"
    "(?P<course>\d+[A-Z]?\s+|---\s+|[A-F1-4\/]+\.? +)?"
    "(?P<description>.+?\n?.+? *)"
    "(?P<attemptedCredits>[\d.]+ +)"
    "(?P<earnedCredits>[\d.]+ +)"
    "(?P<grade>[A-DFIW]\s+|WU\/U +|AU +|CR +|NC +|RD +|RP +|WE +|\d+ +)"
    "(?P<points>[\d.]+)")
    
    # Split the document text by educational institution. "Test Credits" is considered an educational institution
    # Returned list will be institution name followed by document text related to the given institution
    splitByInstitution = re.split(regexPatternTransferInstitution, transcriptContents)
    # Deals with the test credits:
    lastTextBlock = splitByInstitution.pop()
    splitTestCredits = lastTextBlock.split("Test Credits", maxsplit=1)
    if len(splitTestCredits) > 1:
        splitByInstitution.append(splitTestCredits[0])
        splitByInstitution.append("Test Credits")
        splitByInstitution.append(splitTestCredits[1])
    else:
        splitByInstitution.append(lastTextBlock)
    # Deals with the CSU Long Beach section of the transcript:
    lastTextBlock = splitByInstitution.pop()
    splitUndergrad = lastTextBlock.split("Beginning of Undergraduate  Record")
    if len(splitUndergrad) > 1:
        splitByInstitution.append(splitUndergrad[0])
        splitByInstitution.append("California State University, Long Beach")
        splitByInstitution.append(splitUndergrad[1])
    else:
        splitByInstitution.append(lastTextBlock)


    output: str = ""
    for i in range(1, len(splitByInstitution), 2):
        institution: str = splitByInstitution[i]
        textBlock: str = splitByInstitution[i + 1]

        output += "\nCourses attended at " + institution + "\n================================\n"

        regexMatchesCourses = re.finditer(regexPatternCourse, textBlock)

        for match in regexMatchesCourses:
            groupDict = match.groupdict()
            for key in groupDict:
                value = groupDict[key]
                if value != None:
                    groupDict[key] = groupDict[key].strip().replace("\n", "")
            output += groupDict["department"].ljust(6) +\
                      groupDict["course"].ljust(6) +\
                      groupDict["description"].ljust(40) +\
                      groupDict["attemptedCredits"].ljust(6) +\
                      groupDict["earnedCredits"].ljust(6) +\
                      groupDict["grade"].ljust(6) +\
                      groupDict["points"].rjust(7) + " ";
            repeated = groupDict["repeated"]
            if repeated != None:
                      output += repeated
            output += "\n"
    return output

