'''
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
'''

def check_citation(output):
return "chunk" in output.lower()

def check_abstention(output):
return "i don't know" in output.lower()

def check_structure(output):
return all(x in output for x in [
"Decision",
"Answer",
"Why",
"Citations"
])

def evaluate(outputs):
total = len(outputs)

```
citation_score = sum(check_citation(o) for o in outputs)
abstain_score = sum(check_abstention(o) for o in outputs)
structure_score = sum(check_structure(o) for o in outputs)

print(f"Citation Coverage: {citation_score/total}")
print(f"Abstention Accuracy: {abstain_score/total}")
print(f"Structure Compliance: {structure_score/total}")
```
