import json

test_cases = {}

# TestFormatResponse
texts = {   "code_block_containing_boldened_text": "```python\n**boldened**\n```**boldened**",
"code_block_multiple": "```python\nCode\n```\nText\n```C++\nCode\n```\nText",
"code_block_containing_italicized_text": "```python\nHey, some *code*\n```",
"inline_code_single": "text`**not bold**` text",
"inline_code_multiple": "text`**not bold**` text `*not italic*`",
"inline_code_multi_line_single": "text `text \n**bold**`",
"inline_code_multi_line_multiple": "text `code \n**bold**`\n`**notbold**`",
"bullet_list_multi_line": '''
* 1 cup red lentils, rinsed
* 2 cups water or vegetable broth
* 1 tbsp oil
* 1 tsp ground cumin
* 1 tsp ground coriander
* ½ tsp turmeric powder
* ½ tsp garam masala
* ¼ tsp cayenne pepper (optional)
* 1 small onion, chopped
* 2 cloves garlic, minced
* 1 inch ginger, grated
* Salt to taste
* Fresh cilantro, chopped (for garnish)''', 
"bullet_list_multi_line_indented": '''1. Test CMake Directly:
* Install CMake independently of Homebrew (e.g., from the CMake website's official macOS distribution).  
* Create a simple CMake project (e.g., `CMakeLists.txt` containing `cmake_minimum_required(VERSION 3.10) project(MyProject) add_executable(MyProject main.cpp)`, and `main.cpp` containing a basic "Hello, world!" program).
* Try to build it using the independently installed CMake from the command line. This helps determine if CMake itself is malfunctioning.''',
"bullet_item": "\n* Large pot or Dutch oven",
"bullet_item_boldened_text_normal_text": "\n* **Boldened Text** Unboldened text.",
"bullet_item_boldened_italic_text": "\n* ***Boldened Italic.***",
"bullet_item_boldened_text_asterisks": "\n* * **Boldened NOT Italic.** *",
"bullet_item_indented": "\n    * A",
"bullet_item_asterisk": "\n* Dial *555",
"italic_text_containing_boldened_text": "*Italic **bold-italic** Italic*",
"boldened_italic_close": "***Hey***",
}
f_texts = { "code_block_containing_boldened_text": "\tpython: - - - - -\n**boldened**\n\t- - - - - - - - - -\033[39;49;1mboldened\033[22m",
"code_block_multiple": "\tpython: - - - - -\nCode\n\t- - - - - - - - - -\nText\n\tC++: - - - - -\nCode\n\t- - - - - - - - - -\nText",
"code_block_containing_italicized_text": "\tpython: - - - - -\nHey, some *code*\n\t- - - - - - - - - -",
"inline_code_single": "text`**not bold**` text",
"inline_code_multiple": "text`**not bold**` text `*not italic*`",
"inline_code_multi_line_single": "text `text \n\033[39;49;1mbold\033[22m`",
"inline_code_multi_line_multiple": "text `code \n\033[39;49;1mbold\033[22m`\n`**notbold**`",
"bullet_list_multi_line": '''
- 1 cup red lentils, rinsed
- 2 cups water or vegetable broth
- 1 tbsp oil
- 1 tsp ground cumin
- 1 tsp ground coriander
- ½ tsp turmeric powder
- ½ tsp garam masala
- ¼ tsp cayenne pepper (optional)
- 1 small onion, chopped
- 2 cloves garlic, minced
- 1 inch ginger, grated
- Salt to taste
- Fresh cilantro, chopped (for garnish)''',
"bullet_list_multi_line_indented": '''1. Test CMake Directly:
- Install CMake independently of Homebrew (e.g., from the CMake website's official macOS distribution).  
- Create a simple CMake project (e.g., `CMakeLists.txt` containing `cmake_minimum_required(VERSION 3.10) project(MyProject) add_executable(MyProject main.cpp)`, and `main.cpp` containing a basic "Hello, world!" program).
- Try to build it using the independently installed CMake from the command line. This helps determine if CMake itself is malfunctioning.''',
"bullet_item": "\n- Large pot or Dutch oven",
"bullet_item_boldened_text_normal_text": "\n- \033[39;49;1mBoldened Text\033[22m Unboldened text.",
"bullet_item_boldened_italic_text": "\n- \033[39;49;1m\033[39;49;3mBoldened Italic.\033[22m\033[23m",
"bullet_item_boldened_text_asterisks": "\n- * \033[39;49;1mBoldened NOT Italic.\033[22m *",
"bullet_item_indented": "\n    - A",
"bullet_item_asterisk": "\n- Dial *555",
"italic_text_containing_boldened_text": "\033[39;49;3mItalic \033[39;49;1mbold-italic\033[22m Italic\033[23m",
"boldened_italic_close": "\033[39;49;1m\033[39;49;3mHey\033[22m\033[23m",
}

test_cases["TestFormatResponse"] = {"texts": texts, "f_texts": f_texts}

# TestGeminiFormatHelperFunctions
texts = {
"bullet-complex": "* **Text",
"bullet-streamed": "*\nText",
"bullet-multiline": "* Text\n* Text",
"bullet-multiline-streamed": "*\nText\n*\nText",
"bullet-indented-tab": "\t* Text",
"bullet-indented-spaces": "\n    * Text",
"numbered_lists-item": "**1.",
"numbered_lists-list": "**1. Text\n**2. Text",
"header-1": "\t# Header 1 #",
"header-1-not": "\t # Header",
"bold_text-simple": "**Text**",
"bold_text-not": "** * Text ***",
"simple_math-mult-A": "5 * 10 = 9",
"simple_math-mult-B": "5*10 = 9",
"simple_math-mult-B": "5*10 * 3 = 9",
"simple_math-mult-C": "5*10*3 = 9",
"italicized_text-one-char": "The number *e*, approximately",
"italicized_text-asterisks": " *** ",
"italicized_text-sentence-with-asterisks": "Hey * this is not * italicized",
"italicized_text-sentence-with-asterisks-B": "Hey *this is not * italicized",
"italicized_text-sentence": "Hey *this is* italicized",
"italicized_text-sentence-with-asterisk": "Hey *this is* also* italicized",
"italicized_text-asterisk-inside-word": "'*args' text '*args'.",
"italicized_text-italicized-asterisk-inside-word": "**args* text '*args'.",
"italicized_text-asterisk-in-word-sentence": "`*args`: The `*args` syntax in your `calculate` function definition means *it can accept a variable number of positional arguments*.  These arguments are packed into a tuple named `*args` inside the function."
}
f_texts = {
"bullet-complex": "- Text",
"bullet-streamed": "- Text",
"bullet-multiline": "- Text\n- Text",
"bullet-multiline-streamed": "- Text\n- Text",
"bullet-indented-spaces": "\n    - Text",
"bullet-indented-tab": "\t- Text",
"numbered_lists-item": "1.",
"numbered_lists-list": "1. Text\n2. Text",
"header-1": "\t\t Header 1 #",
"header-1-not": "\t # Header",
"bold_text-simple": "\033[39;49;1mText\033[22m",
"bold_text-not": "\033[39;49;1m * Text *\033[22m",
"simple_math-mult-A": "5 * 10 = 9",
"simple_math-mult-B": "5*10 = 9",
"simple_math-mult-B": "5*10 * 3 = 9",
"simple_math-mult-C": "5*10*3 = 9",
"italicized_text-one-char": "The number \033[39;49;3me\033[23m, approximately",
"italicized_text-asterisks": " *** ",
"italicized_text-sentence-with-asterisks": "Hey * this is not * italicized",
"italicized_text-sentence-with-asterisks-B": "Hey *this is not * italicized",
"italicized_text-sentence": "Hey \033[39;49;3mthis is\033[23m italicized",
"italicized_text-sentence-with-asterisk": "Hey \033[39;49;3mthis is\033[23m also* italicized",
"italicized_text-asterisk-inside-word": "'*args' text '*args'.",
"italicized_text-italicized-asterisk-inside-word": "*\033[39;49;3margs\033[23m text '*args'.",
"italicized_text-asterisk-in-word-sentence": "`*args`: The `*args` syntax in your `calculate` function definition means \033[39;49;3mit can accept a variable number of positional arguments\033[23m.  These arguments are packed into a tuple named `*args` inside the function."
}

test_cases["TestGeminiFormatHelperFunctions"] = {"texts": texts, "f_texts": f_texts}

# TestOpenaiFormatHelperFunctions
texts = {
'bullet-streamed': '*\nText',
'bullet-multiline': '* Text\n* Text',
'bullet-multiline-streamed': '*\nText\n*\nText',
'bullet-indented-tab': '\t* Text',
'bullet-indented-spaces': '\n    * Text',
'bold_text-simple': '**Text**',
'bold_text-not': '** * Text ***',
'simple_math-mult-A': '5 * 10 = 9',
'simple_math-mult-B': '5*10 = 9',
'simple_math-mult-B': '5*10 * 3 = 9',
'simple_math-mult-C': '5*10*3 = 9',
'italicized_text-one-char': 'The number *e*, approximately',
'italicized_text-asterisks': ' *** ',
'italicized_text-sentence-with-asterisks': 'Hey * this is not * italicized',
'italicized_text-sentence-with-asterisks-B': 'Hey *this is not * italicized',
'italicized_text-sentence': 'Hey *this is* italicized',
'italicized_text-sentence-with-asterisk': 'Hey *this is* also* italicized',
'italicized_text-asterisk-inside-word': "'*args' text '*args'.",
'italicized_text-italicized-asterisk-inside-word': "**args* text '*args'.",
'italicized_text-asterisk-in-word-sentence': "`*args`: The `*args` syntax in your `calculate` function definition means *it can accept a variable number of positional arguments*.  These arguments are packed into a tuple named `*args` inside the function."
}
f_texts = {
'bullet-streamed': '- Text',
'bullet-multiline': '- Text\n- Text',
'bullet-multiline-streamed': '- Text\n- Text',
'bullet-indented-spaces': '\n    - Text',
'bullet-indented-tab': '\t- Text',
'bold_text-simple': '\033[39;49;1mText\033[22m',
'bold_text-not': '\033[39;49;1m * Text *\033[22m',
'simple_math-mult-A': '5 * 10 = 9',
'simple_math-mult-B': '5*10 = 9',
'simple_math-mult-B': '5*10 * 3 = 9',
'simple_math-mult-C': '5*10*3 = 9',
'italicized_text-one-char': 'The number \033[39;49;3me\033[23m, approximately',
'italicized_text-asterisks': ' *** ',
'italicized_text-sentence-with-asterisks': 'Hey * this is not * italicized',
'italicized_text-sentence-with-asterisks-B': 'Hey *this is not * italicized',
'italicized_text-sentence': 'Hey \033[39;49;3mthis is\033[23m italicized',
'italicized_text-sentence-with-asterisk': 'Hey \033[39;49;3mthis is\033[23m also* italicized',
'italicized_text-asterisk-inside-word': "'*args' text '*args'.",
'italicized_text-italicized-asterisk-inside-word': "*\033[39;49;3margs\033[23m text '*args'.",
'italicized_text-asterisk-in-word-sentence': "`*args`: The `*args` syntax in your `calculate` function definition means \033[39;49;3mit can accept a variable number of positional arguments\033[23m.  These arguments are packed into a tuple named `*args` inside the function."
}

test_cases["TestOpenaiFormatHelperFunctions"] = {"texts": texts, "f_texts": f_texts}

with open("api_session.json", mode="w") as json_file:
    json_file.write(json.dumps(test_cases, ensure_ascii=False))