# LLM-Based Test Refactoring with Chain-of-Thought Prompting

This folder contains the full pipeline for refactoring automatically generated unit test suites using two Large Language Models: **GPT-4o** and **Mistral-Large-2407**. The process applies Chain-of-Thought (CoT) prompting to enhance **readability**, **naming**, **structure**, and **modularity**, while strictly **preserving functional behavior**.

This pipeline supports batch processing and was used to generate the refactored test suites evaluated in our paper:

> **Beyond CodeBLEU: Rethinking Test Refactoring Evaluation with Semantics-Driven and Behavior-Preserving Metrics**  

---

## Objective

The refactoring process addresses key challenges in test quality evaluation. While tools like EvoSuite generate tests with valid logic, the output is often synthetic and hard to read. Our goal is to use LLMs to:

- Improve naming and structure without changing behavior
- Add **Given–When–Then** documentation
- Remove trivial test smells (long names, over-assertion, etc.)
- Prepare test suites for downstream maintainability and evaluation (e.g., CTSES metric)

---

## Folder Structure

```
Refactored-Test-Suite-Code/
├── DATASET/                       # JSON files with EvoSuite test code and static headers
│   ├── Defects4J_part1.json
│   ├── Defects4J_part2.json
│   ├── Defects4J_part3.json
│   ├── SF110_part1.json
│   ├── SF110_part2.json
│   └── SF110_part3.json
├── gpt-scenario-1.sh             # Batch launcher for GPT-4o scripts
├── mistral-scenario-1.sh         # Batch launcher for Mistral scripts
├── gpt-scenario1-part{1,2,3}.py  # GPT-4o refactoring scripts (parallelizable)
├── mistral-scenario1-part{1,2,3}.py  # Mistral refactoring scripts (parallelizable)
└── README.md
```

---

## Models & Configurations

- **GPT-4o** via OpenAI API (`tiktoken`, temperature = 0.1, max tokens = 128k)
- **Mistral-Large-2407** via Mistral API (temperature = 0.1, max retries = 30)

Both models use a **Chain-of-Thought prompt** to guide the LLM through a multi-step refactoring task:

1. Understand test intent and purpose  
2. Analyze dependencies  
3. Rename and restructure  
4. Add Given–When–Then comments  
5. Review for correctness  

---

## Running the Refactoring Pipeline

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Then launch the batch scripts in parallel:

```bash
bash gpt-scenario-1.sh
bash mistral-scenario-1.sh
```

Each `.sh` script will:

- Launch 3 parallel Python scripts to handle part1, part2, and part3 of the dataset  
- Track progress via `.flag` files per iteration  
- Retry on failure, log OpenAI/Mistral API errors  
- Produce output files in: `Refactoring-output/Scenario-1/{GPT|MISTRAL}/...`  

---

## Dataset Strategy

- Defects4J and SF110 datasets were split into 3 parts each to allow parallelization  
- Each test suite was refactored over 3 iterations  
- Output files include iteration ID, project name, bug ID (if applicable), and class name  

---

## Prompt Constraints

LLMs are explicitly instructed to:

- Retain static EvoSuite elements (package/imports/class signature)  
- Preserve all original test logic and assertions  
- Focus only on improving human readability  

Prompt excerpts include:

```
Constraints:
- Do Not Alter: Retain EvoSuite-specific elements
- Preserve Functionality
- Add Given-When-Then Comments

Steps:
1. Understand the intent and context of the test suite.
2. Refactor methods: rename clearly, restructure with comments.
```

---

## Output Format

Each refactored file is stored in:

```
Refactoring-output/Scenario-1/{GPT|MISTRAL}/{Dataset}/{Project}/{Class}/[bug-id]/testsuite_{id}/
└── [iteration_id]-[project]-[bug-id]-[class]-refactoring-output-iter-{n}.txt
```

---

## Paper Configuration Reference

This setup corresponds to Section III-A of the paper:

- **Test Generation**: EvoSuite with DynaMOSA, 15 iterations/class, 3min timeout  
- **Test Refactoring**: 3 refactorings per test using GPT-4o and Mistral-Large-2407  
- Only compilable outputs are retained  

---

## References

- Fraser & Arcuri. *EvoSuite: automatic test suite generation*, FSE 2011.  
- Wei et al. *Chain-of-Thought prompting elicits reasoning*, NeurIPS 2022.  
- OpenAI. *GPT-4o System Card*, 2024.  
- Mistral AI. *Mistral-Large-2407*, 2024.  
