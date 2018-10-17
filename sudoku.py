#!/usr/bin/env python3
import gi.repository
gi.require_version('Gtk','3.0')
from gi.repository import Gtk

class AppWin(Gtk.Window):
	def blank_sudoku(self):
		m=[]
		for i in range(3):
			m.append([])
			for j in range(3):
				m[i].append([])
				for k in range(3):
					m[i][j].append([0,0,0])
		return m[:]
	
	def blank_markup(self):
		mk=[]
		for i in range(3):
			mk.append([])
			for j in range(3):
				mk[i].append([])
				for k in range(3):
					mk[i][j].append([{x for x in range(1,10)},{x for x in range(1,10)},{x for x in range(1,10)}])
		return mk[:]
	
	def is_in_row(self,num,R,r,av1,av2,s):
		result=False
		for i,j in [(x,y) for x in range(3) for y in range(3) if x!=av1 or y!=av2]:
			if num==s[R][i][r][j]:
				result=True
				return result
		return result
	
	def is_in_column(self,num,C,c,av1,av2,s):
		result=False
		for i,j in [(x,y) for x in range(3) for y in range(3) if x!=av1 or y!=av2]:
			if num==s[i][C][j][c]:
				result=True
				return result
		return result
	
	def is_in_box(self,num,R,C,av1,av2,s):
		result=False
		for i,j in [(x,y) for x in range(3) for y in range(3) if x!=av1 or y!=av2]:
			if num==s[R][C][i][j]:
				result=True
				return result
		return result
	
	def is_valid_markup(self,mk):
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			if mk[i][j][k][l]==set():
				return False
		return True
	
	def is_valid_sudoku(self,s):
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			num=s[i][j][k][l]
			if num!=0 and (self.is_in_row(num,i,k,j,l,s) or self.is_in_column(num,j,l,i,k,s) or self.is_in_box(num,i,j,k,l,s)):
				return False
		return True
	
	def number_of_blanks(self,s):
		count=0
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			if s[i][j][k][l]==0:
				count+=1
		return count
	
	def generate_markup(self,s,mk):
		m=mk[:]
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			if s[i][j][k][l]!=0:
				m[i][j][k][l]={s[i][j][k][l]}
			else:
				temp=set(mk[i][j][k][l])
				for num in temp:
					if self.is_in_row(num,i,k,3,3,s) or self.is_in_column(num,j,l,3,3,s) or self.is_in_box(num,i,j,3,3,s):
						m[i][j][k][l].discard(num)
		return m[:]
	
	def candidate_check(self,s):
		check=True
		while check:
			change=0
			for R,C in [(x,y) for x in range(3) for y in range(3)]:
				for r,c in [(x,y) for x in range(3) for y in range(3) if s[R][C][x][y]==0]:
					temp={x for x in range(1,10)}
					d=set()
					for num in temp:
						for i,j in [(x,y) for x in range(3) for y in range(3) if (x!=r or y!=c)]:
							d=d.union({s[R][C][i][j]})
						for i,j in [(x,y) for x in range(3) for y in range(3) if (x!=C or y!=c)]:
							d=d.union({s[R][i][r][j]})
						for i,j in [(x,y) for x in range(3) for y in range(3) if (x!=R or y!=r)]:
							d=d.union({s[i][C][j][c]})
					pos=set.difference(temp,d)
					if len(pos)==1:
						s[R][C][r][c]=list(pos)[0]
						change+=1
			if change==0:
				check=False
		return s[:]
	
	def place_finding(self,s):
		ch=False
		for i,j in [(x,y) for x in range(3) for y in range(3)]:
			for num in [x for x in range(1,10)]:
				if self.is_in_row(num,i,j,3,3,s):
					continue
				else:
					a=[]
					for k,l in [(x,y) for x in range(3) for y in range(3)]:
						if s[i][k][j][l]!=0:
							continue
						elif self.is_in_column(num,k,l,3,3,s):
							continue
						elif self.is_in_box(num,i,k,3,3,s):
							continue
						else:
							a.append((i,k,j,l))
					if len(a)==1:
						s[a[0][0]][a[0][1]][a[0][2]][a[0][3]]=num
						ch=True
						return [s[:],ch]
	
		for i,j in [(x,y) for x in range(3) for y in range(3)]:
			for num in [x for x in range(1,10)]:
				if self.is_in_column(num,i,j,3,3,s):
					continue
				else:
					a=[]
					for k,l in [(x,y) for x in range(3) for y in range(3)]:
						if s[k][i][l][j]!=0:
							continue
						elif self.is_in_row(num,k,l,3,3,s):
							continue
						elif self.is_in_box(num,k,i,3,3,s):
							continue
						else:
							a.append((k,i,l,j))
					if len(a)==1:
						s[a[0][0]][a[0][1]][a[0][2]][a[0][3]]=num
						ch=True
						return [s[:],ch]
	
		for i,j in [(x,y) for x in range(3) for y in range(3)]:
			for num in [x for x in range(1,10)]:
				if self.is_in_box(num,i,j,3,3,s):
					continue
				else:
					a=[]
					for k,l in [(x,y) for x in range(3) for y in range(3)]:
						if s[i][j][k][l]!=0:
							continue
						elif self.is_in_row(num,i,k,3,3,s):
							continue
						elif self.is_in_column(num,j,l,3,3,s):
							continue
						else:
							a.append((i,j,k,l))
					if len(a)==1:
						s[a[0][0]][a[0][1]][a[0][2]][a[0][3]]=num
						ch=True
						return [s[:],ch]
		return [s[:],ch]
	
	def backtrack(self,s,mk):
		ss=self.copy_sudoku(s)
		mm=self.copy_markup(mk)
		if self.number_of_blanks(ss)==0:
			return [ss,mm,True]
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			if s[i][k][j][l]==0:
				w,x,y,z=i,k,j,l
				break
		for num in mk[w][x][y][z]:
			ss[w][x][y][z]=num
			mm=self.generate_markup(ss[:],mm[:])
			if self.is_valid_sudoku(ss) and self.is_valid_markup(mm):
				if self.number_of_blanks(ss)!=0:
					[tt,nn,check]=self.backtrack(ss,mm)
					if check:
						ss=tt
						mm=nn
						return [ss,mm,True]
					else:
						ss=self.copy_sudoku(s)
						mm=self.copy_markup(mk)
						continue
				else:
					return [ss,mm,True]
			else:
				ss=self.copy_sudoku(s)
				mm=self.copy_markup(mk)
		return [ss,mm,False]
	
	def copy_sudoku(self,s):
		m=self.blank_sudoku()
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			m[i][j][k][l]=s[i][j][k][l]
		return m[:]
	
	def copy_markup(self,m):
		a=self.blank_markup()
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			a[i][j][k][l]=set.copy(m[i][j][k][l])
		return a[:]
	
	def Solve(self,event):
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			t=self.sg[i][j][k][l].get_text()
			if t!='':
				self.s[i][j][k][l]=int(t)
			else:
				self.s[i][j][k][l]=0
		mark=self.blank_markup()
		t=True
		while t:
			self.s=self.candidate_check(self.s[:])
			[s,t]=self.place_finding(self.s[:])
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			self.sg[i][j][k][l].set_text(str(self.s[i][j][k][l]))
		mark=self.generate_markup(self.s[:],mark[:])
		[self.s,mark,check]=self.backtrack(self.s[:],mark[:])
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			self.sg[i][j][k][l].set_text(str(self.s[i][j][k][l]))
	
	def Reset(self,event):
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			self.sg[i][j][k][l].set_text('')
		self.s=self.blank_sudoku()

	def __init__(self):
		Gtk.Window.__init__(self,title='Solve Sudokus')
		self.set_default_size(400,200)
		self.set_hexpand(False)
		self.connect('delete-event',Gtk.main_quit)
		self.sudoku=Gtk.Grid(border_width=1,column_spacing=1,row_spacing=2)
		self.add(self.sudoku)
		self.createSudoku()
		self.show_all()
	
	def createSudoku(self):
		self.sg=self.blank_sudoku()
		self.s=self.blank_sudoku()
		for i,j,k,l in [(w,x,y,z) for w in range(3) for x in range(3) for y in range(3) for z in range(3)]:
			self.sg[i][j][k][l]=Gtk.Entry(width_chars=3,xalign=0.5)
			self.sudoku.attach(self.sg[i][j][k][l],3*j+l,3*i+k,1,1)
		self.solve=Gtk.Button(label='Solve')
		self.solve.connect('clicked',self.Solve)
		self.reset=Gtk.Button(label='Reset')
		self.reset.connect('clicked',self.Reset)
		self.sudoku.attach(self.solve,9,3,1,1)
		self.sudoku.attach(self.reset,9,5,1,1)

app=AppWin()
Gtk.main()
