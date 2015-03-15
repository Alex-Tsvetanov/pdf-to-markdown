# -*- coding: utf8 -*-

import os

class Writer(object):
	def __init__(self):
		self._mode = 'simple'
		self._title = 'markdown'


	def set_syntax(self, syntax):
		self._syntax = syntax


	def set_mode(self, mode):
		self._mode = mode


	def set_title(self, title):
		self._title = title


	def write(self, piles):
		if self._mode == 'simple':
			self._write_simple(piles)
		elif self._mode == 'gitbook':
			self._write_gitbook(piles)


	def _write_simple(self, piles):
		filename = self._title + '.md'
		with open(filename, 'w') as fwrite:
			for pile in piles:
				if pile.get_type() == 'image':
					image = pile.get_image()
					self._save_image(image, 'images')
				markdown = pile.gen_markdown(self._syntax)
				fwrite.write(markdown)


	def _write_gitbook(self, piles):
		intermediate = self._gen_gitbook_intermediate(piles)
		self._write_gitbook_from_intermediate(intermediate)


	def _gen_gitbook_intermediate(self, piles):
		return {
			'title': '臺北市內湖區都市計畫通盤檢討（主要計畫）案',
			'readme': '# 臺北市政府',
			'chapters': [
				{
					'title': '前言',
					'readme': '# 前言',
					'sections': [
						{
							'title': '緣起',
							'content': '# 緣起'
						},
						{
							'title': '檢討目的',
							'content': '# 檢討目的'
						},
						{
							'title': '計畫範圍與年期',
							'content': '# 計畫範圍與年期'
						},
					]
				},
				{
					'title': '都市計畫發布情形',
					'readme': '# 都市計畫發布情形',
					'sections': [
						{
							'title': '原都市計畫情形',
							'content': '# 原都市計畫情形'
						},
					]
				},
				{
					'title': '都市發展現況',
					'readme': '# 都市發展現況',
					'sections': [
						{
							'title': '自然環境概況',
							'content': '# 自然環境概況'
						},
						{
							'title': '社經發展概況',
							'content': '# 社經發展概況'
						},
					]
				},
			]
		}


	def _mkdir_anyway(self, dirname):
		if not os.path.exists(dirname):
			os.makedirs(dirname)


	def _write_gitbook_from_intermediate(self, intermediate):
		book_dirname = self._title
		self._mkdir_anyway(book_dirname)
		self._write_gitbook_summary(book_dirname, intermediate)
		self._write_gitbook_content(book_dirname, intermediate)


	def _write_gitbook_summary(self, book_dirname, intermediate):
		lines = []
		chapters = intermediate['chapters']
		for idx, chapter in enumerate(chapters):
			line = '* [{}](chapter-{}/README.md)'.format(chapter['title'], idx)
			lines.append(line)
			sections = chapter['sections']
			for jdx, section in enumerate(sections):
				line = '\t* [{}](chapter-{}/section-{}.md)'.format(section['title'], idx, jdx)
				lines.append(line)

		self._write_gitbook_file(os.path.join(book_dirname, 'SUMMARY.md'), '\n'.join(lines))


	def _write_gitbook_content(self, book_dirname, intermediate):
		self._write_gitbook_file(os.path.join(book_dirname, 'README.md'), intermediate['readme'])

		chapters = intermediate['chapters']
		for idx, chapter in enumerate(chapters):
			chapter_dirname = os.path.join(book_dirname, 'chapter-{}'.format(idx))
			self._mkdir_anyway(chapter_dirname)
			self._write_gitbook_file(os.path.join(chapter_dirname, 'README.md'), chapter['readme'])

			sections = chapter['sections']
			for jdx, section in enumerate(sections):
				section_filename = 'section-{}.md'.format(jdx)
				self._write_gitbook_file(os.path.join(chapter_dirname, section_filename), section['content'])


	def _write_gitbook_file(self, filename, content):
		with open(filename, 'w') as fwrite:
			fwrite.write(content)


	def _save_image(self, image, dirname):
		self._mkdir_anyway(dirname)

		result = None
		if not image.stream:
			raise Exception('No stream found')
		stream = image.stream.get_rawdata()
		filename = os.path.join(dirname, image.name)
		with open(filename, 'wb') as fwrite:
			fwrite.write(stream)
			fwrite.close()

