import string
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

def unpunctuate(s):
	exclude = set(string.punctuation)
	unpunc = ''.join(ch for ch in s if ch not in exclude)
	return unpunc

def remove_function_words(s):
	s_list = s.split(' ')
	filtered_list = [w for w in s_list if w not in stopwords.words('english')]
	s = ' '.join(filtered_list)
	return s

def stem(s):
	st = LancasterStemmer()
	s_list = s.split(' ')
	stem_list = [st.stem(w) for w in s_list]
	s = ' '.join(stem_list)
	return s

def preprocess(s):
	s = unpunctuate(s)
	s = s.lower()
	s = remove_function_words(s)
	s = stem(s)
	return s	

def main():
	file_list = ['lec26.pdf.xmln1','Agile software development1']
	with open('sentences.txt','w') as f:
		for item in file_list:
			with open(item) as fo:
				text = fo.read()
			# print text
			paras = text.split('<p>')
			for para in paras[:-1]: 				# the last split is a blank line and not taken
				para = para.strip('\n')
				sentences = para.split('<s>')
				for sentence in sentences:
					sentence = preprocess(sentence)
					sentence.strip(' ')
					f.write(sentence+'\n')

main()