def check_citation(output):
return "Citations:" in output

def check_abstention(output):
return "I don't know" in output

def evaluate(outputs):
total = len(outputs)


citation_count = sum(check_citation(o) for o in outputs)
abstain_count = sum(check_abstention(o) for o in outputs)

print("Citation Coverage:", citation_count / total)
print("Abstention Rate:", abstain_count / total)


