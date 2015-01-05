__author__ = 'hooda'

# The	Partition	Problem:	You	are	given	a	set	of	� (assume	� ≤ 1000)	objects	� = �!, … , �! and	a
# symmetric	 dissimilarity function	 �: �×� → {0,1, … , �} (assume	 � ≤ 10000).	 The	 value
# � �!, �! = �(�!, �!) denotes	the	measure	of	dissimilarity	between	objects	�! and �!.	You	may
# assume	that	� �!, �! = 0 for	all	�.	Your	goal	is	to	partition	these	objects	into	two	sets	� and	�
# such	that	� � + �(�) is	minimized,	where	the	function	� is	defined	as:
# ∀� ⊆ �, � � = ���!!,!!∈!{� �!, �! }
# INPUT:	 The	 first	 line	 of	 the	 input	 is	 the	 value	 �. This	 is	 followed	 by	 � − 1 lines.	 The	�
# !! line
# among	 these, give	 the	 dissimilarity	 value	 of	 the	 �
# !! object	 with	 objects	 � + 1, � + 2, … , �
# (separated	by	commas).	Below,	we	give	an	example	input	file	(“input.txt”).
# 5
# 4,5,0,2
# 1,3,8
# 2,0
# 4
# OUTPUT:	The	first	line	of	the	output	should	be	the	minimum	value	of	� � + �(�).	The	next	two
# lines	 should	 give	 such sets	� and	� (in	 terms	 of	 the	indices	 of	 objects	 separated	 by	 comma).
# Below	we	give	an	example	output	file. Below	is	the	output	file	corresponding	to	the	above	input
# file.
# 4
# 1,2,4
# 3,5

