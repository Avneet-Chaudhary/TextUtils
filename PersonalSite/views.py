from django.http import HttpResponse
from django.shortcuts import render
import re

# This view renders the index page
def index(request):
    return render(request, 'index.html')

# This view handles the text analysis operations
def analyze(request):
    # Get the input text from the form, default to 'default'
    texxt = request.POST.get('text', 'default')

    # Get the status of various operations from the form
    removepunc = request.POST.get('removepunc', 'off')
    uppercase = request.POST.get('fullcaps', 'off')
    newlineRemover = request.POST.get('newlineRemover', 'off')
    spaceremover = request.POST.get('spaceremover', 'off')
    charCount = request.POST.get('charCount', 'off')

    # Perform punctuation removal if requested
    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in texxt:
            if char not in punctuations:
                analyzed = analyzed + char
        params = {'purpose': 'Removed Punctuations', 'analyzed_text': analyzed}
        texxt = analyzed

    # Convert text to uppercase if requested
    if uppercase == "on":
        string_in_upper = texxt.upper()
        params = {'purpose': 'Changed to Uppercase', 'analyzed_text': string_in_upper}
        texxt = string_in_upper

    # Remove newlines if requested
    if newlineRemover == "on":
        without_newline = re.sub(r'[\r\n]+', '', texxt)
        params = {'purpose': 'New Line Remover', 'analyzed_text': without_newline}
        texxt = without_newline

    # Remove spaces if requested
    if spaceremover == "on":
        text_without_space = texxt.replace(" ", "")
        params = {'purpose': 'Space Remover', 'analyzed_text': text_without_space}
        texxt = text_without_space

    # Count characters if requested
    if charCount == "on":
        count = len(texxt)
        params = {'purpose': 'Count of Chars', 'analyzed_text': count}

    # If no operation is selected, display a message
    if (
            removepunc != "on" and newlineRemover != "on" and uppercase != "on" and charCount != "on" and spaceremover != "on"):
        return HttpResponse("Please select an option to perform an operation")

    # Render the analyze.html template with the appropriate parameters
    return render(request, 'analyze.html', params)
