import TranscriptParser

def WriteClassListToTextFile(transcriptFilePath: str, textFilePath: str):
    # Make sure the text file is empty
    textFile = open(textFilePath, "w")
    textFile.close()

    parsed = TranscriptParser.GetClassList(transcriptFilePath)
    textFile = open(textFilePath, "w")
    textFile.write(parsed)
    textFile.close()

def WriteTranscriptContentsToTextFile(transcriptFilePath: str, textFilePath: str):
    # Make sure the text file is empty
    textFile = open(textFilePath, "w")
    textFile.close()

    contents = TranscriptParser.GetTranscriptText(transcriptFilePath)
    textFile = open(textFilePath, "w")
    textFile.write(contents)
    textFile.close()

#output = TranscriptParser.ValidateTranscript("testFiles/transcript2.pdf")
#print(output)

WriteClassListToTextFile("testFiles/transcript1.pdf", "testFiles/test.txt")
# WriteTranscriptContentsToTextFile("testFiles/transcript2.pdf", "testFiles/output2.txt")2``