__author__ = 'hooda'

import xml.etree.ElementTree as eTree
import xml.dom.minidom as minidom
from itertools import product


class InvalidXML(Exception):
    pass


class InvalidFormula(Exception):
    pass


# The base class for a formula. Not actually supposed to be instanced and used.
# The functions are all standing in for actual implementation by subclasses.
# Documented here for convenience.
class Formula:
    def __init__(self, data):
        self.data = data

    def vars(self):
        """
        Used to access the variables (literals) that occur in the formula.
        This will be needed when trying to generate truth tables for equivalence checking.
        :return: List of variables in this formula.
        """
        return list(set(self.data.vars()))

    def eval(self, table):
        """
        Takes input a table that specifies the truth value for the literals in the formula.
        Substitutes those values and computes whether formula reduced to T or F.
        Obviously table must have all the variables used in the formula.
        :param table: Dictionary of (string, bool)
        :return: Whether the formula evaluates to true or false under the given assignment.
        """
        return self.data.eval(table)

    def __str__(self):
        """
        Used to represent the formula in a readable form instead as object at XYZ.
        Makes for easier debugging.
        :return: A human-readable string of the formula, like (A AND B)
        """
        return str(self.data)

    def __repr__(self):
        return "Formula : " + str(self)

    def __eq__(self, other):
        """
        Overrides equality comparison so that
        x = Formula(stuff)
        y = Formula(stuff)
        are actually considered equal by Python. (By default they're distinct objects at different memory, so unequal)
        :param other: Formula to compare with
        :return: True if and only if the formula has same string representation as the other one, and has same class.
        """
        return isinstance(other, self.__class__) and (str(self) == str(other))
        # return isinstance(other, self.__class__) and (self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """
        Overriding the equality operator makes the Fomula classes unhashable.
        So, this overrides the default hash method. Needed to be able to create sets of formulae.
        :return: Hash of the string representation of the formula.
        """
        return hash(str(self))


# #######################################################################################################################

# Represents a literal, like P.
class Literal(Formula):
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name

    def vars(self):
        return [self.name]

    def eval(self, table):
        return table[self.name]

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Literal : " + str(self)


# #######################################################################################################################

# Represents a negation of a Formula.
class Negation(Formula):
    def __init__(self, a):
        self.a = a

    def vars(self):
        return self.a.vars()

    def eval(self, table):
        return not self.a.eval(table)

    def __str__(self):
        return "(~" + str(self.a) + ")"

    def __repr__(self):
        return "Negation : " + str(self)


# #######################################################################################################################

# Represents the And of two Formula objects (not just two literals)
class And(Formula):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def vars(self):
        return sorted(list(set(self.a.vars() + self.b.vars())))

    def eval(self, table):
        return self.a.eval(table) and self.b.eval(table)

    def __str__(self):
        return "(" + str(self.a) + " AND " + str(self.b) + ")"

    def __repr__(self):
        return "Conjunction : " + str(self)


########################################################################################################################


class Or(Formula):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def vars(self):
        return sorted(list(set(self.a.vars() + self.b.vars())))

    def eval(self, table):
        return self.a.eval(table) or self.b.eval(table)

    def __repr__(self):
        return "Disjunction : " + str(self)

    def __str__(self):
        return "(" + str(self.a) + " OR " + str(self.b) + ")"


########################################################################################################################


class Implies(Formula):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def vars(self):
        return sorted(list(set(self.a.vars() + self.b.vars())))

    def eval(self, table):
        if (self.a.eval(table)) and (not self.b.eval(table)):
            return False
        else:
            return True

    def __str__(self):
        return "(" + str(self.a) + " => " + str(self.b) + ")"

    def __repr__(self):
        return "Implication : " + str(self)


########################################################################################################################


class DoubleImplies(Formula):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def vars(self):
        return sorted(list(set(self.a.vars() + self.b.vars())))

    def eval(self, table):
        return self.a.eval(table) == self.b.eval(table)

    def __str__(self):
        return "(" + str(self.a) + " <=> " + str(self.b) + ")"

    def __repr__(self):
        return "Double Implication : " + str(self)


########################################################################################################################

# Used to represent a set of Formulae.
# The reason I won't go with simply using the inbuilt set is threefold :
# a. Allows me to ensure all objects in this are Formula type.
# b. Makes adding formulae convenient.
# c. Eventually I'll end up with sets of sets of sets ... upto an unknown depth (depending on the original set).
# This allows checking whether I've reached to the lowest level.
class FormulaSet:
    def __init__(self, formulae):
        """
        Takes all objects in the given formulae set(or list), checks that they are of Formula class,
        and adds them so its self.formulae set.
        :param formulae: A set/list of Formula objects.
        """
        self.formulae = set()
        for f in formulae:
            assert isinstance(f, Formula)
            self.formulae = self.formulae.union({f})

    def add(self, f):
        """
        :type f: Formula
        """
        assert isinstance(f, Formula)
        self.formulae.add(f)

    def replace(self, old, new):
        self.formulae.remove(old)
        self.formulae.add(new)

    def split_add(self, old, new1, new2):
        self.formulae.remove(old)
        fset1 = FormulaSet(self.formulae)
        fset2 = FormulaSet(self.formulae)

        fset1.add(new1)
        fset2.add(new2)
        return fset1, fset2

    def union(self, other):
        assert isinstance(other, FormulaSet)
        self.formulae = self.formulae.union(other.formulae)

    def __str__(self):
        s = "{"
        for f in self.formulae:
            s += str(f) + ", "

        if len(s) > 1:
            s = s[:-2]

        return s + "}"

    def __repr__(self):
        return "Set : " + str(self)

    def __eq__(self, other):
        """
        Overrides equality comparison so that
        x = Formula(stuff)
        y = Formula(stuff)
        are actually considered equal by Python. (By default they're distinct objects at different memory, so unequal)
        :param other: Formula to compare with
        :return: True if and only if the formula has same string representation as the other one, and has same class.
        """
        return isinstance(other, self.__class__) and (str(self) == str(other))
        # return isinstance(other, self.__class__) and (self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """
        Overriding the equality operator makes the Fomula classes unhashable.
        So, this overrides the default hash method. Needed to be able to create sets of formulae.
        :return: Hash of the string representation of the formula.
        """
        return hash(str(self))


########################################################################################################################

# Not really supposed to be used. Was to represent sets of sets of formulae.
# But then I'd need a class for sets of sets of sets, and so on. So I'll be using the inbuilt python set for this.
class MultiSet:
    def __init__(self, sets):
        self.sets = set()
        for s in sets:
            assert isinstance(s, FormulaSet)
            self.sets = self.sets.union({s})

    def add(self, s):
        assert isinstance(s, FormulaSet)
        self.sets = self.sets.union({s})

    def union(self, other):
        assert isinstance(other, MultiSet)
        self.sets = self.sets.union(other.sets)

    def __str__(self):
        s = "{"
        for f in self.sets:
            s += str(f) + ", "

        if len(s) > 1:
            s = s[:-2]

        return s + "}"

    def __repr__(self):
        return "Set of Sets : " + str(self)


########################################################################################################################


def parser(infile):
    """

    :param infile: A filename that contains a formula set as given in org_input.xml
    :return: A FormulaSet containing the formulae in the XML file.
    :raise InvalidXMLError: For invalid format of XML.
    """
    tree = eTree.parse(infile)
    root = tree.getroot()

    if root.tag != 'Set':
        raise InvalidXML

    fset = FormulaSet([])

    for element in root:
        #Each set tag has element tags as children. Each element tag will represent a single formula.
        #The element tag has one child, which represents the root operator of its formula.
        fset.add(xml_to_formula(element[0]))

    return fset


def xml_to_formula(e):
    """
    To convert from XML to Formula.
    :rtype : Formula
    :param e: An XML tag, which represents a valid formula. Could be 'Letter', 'Negation', 'Conjunction' etc.
    :return: A Formula subclass object of the formula represented by the XML.
    :raise InvalidXMLError: If the formula is not well formed/wrong tags etc.
    """

    if len(e) == 0 and e.tag == 'Letter':
        return Literal(e.attrib['val'])

    elif len(e) == 1 and e.tag == 'Negation':
        return Negation(xml_to_formula(e[0]))

    elif len(e) == 2:
        if e.tag == 'Disjunction':
            return Or(xml_to_formula(e[0]), xml_to_formula(e[1]))

        elif e.tag == 'Conjunction':
            return And(xml_to_formula(e[0]), xml_to_formula(e[1]))

        elif e.tag == 'Implies':
            return Implies(xml_to_formula(e[0]), xml_to_formula(e[1]))

        elif e.tag == 'Equivalence':
            return DoubleImplies(xml_to_formula(e[0]), xml_to_formula(e[1]))

        else:
            raise InvalidXML

    else:
        raise InvalidXML


def formula_to_xml(f):
    """
    To convert a valid fomula to corresponding XML tag.
    Note : The tag will be of the root operator, not an 'Element' tag.
    :param f:
    :return: :raise AttributeError:
    """
    assert isinstance(f, Formula)

    if isinstance(f, Literal):
        attrib = {'val': f.name}
        return eTree.Element('Letter', attrib)

    elif isinstance(f, Negation):
        n = eTree.Element('Negation')
        n.append(formula_to_xml(f.a))
        return n

    elif isinstance(f, And):
        e1 = formula_to_xml(f.a)
        e2 = formula_to_xml(f.b)
        e = combine(e1, e2, 'Conjunction')
        return e

    elif isinstance(f, Or):
        e1 = formula_to_xml(f.a)
        e2 = formula_to_xml(f.b)

        e = combine(e1, e2, 'Disjunction')
        return e

    elif isinstance(f, Implies):
        e1 = formula_to_xml(f.a)
        e2 = formula_to_xml(f.b)

        e = combine(e1, e2, 'Implies')
        return e

    elif isinstance(f, DoubleImplies):
        e1 = formula_to_xml(f.a)
        e2 = formula_to_xml(f.b)

        e = combine(e1, e2, 'Equivalence')
        return e

    else:
        raise AttributeError


def combine(e1, e2, tag):
    """
    Creates an XML with given tag, and makes e1 and e2 its children.
    :rtype : ElementTree's Element
    """
    e = eTree.Element(tag)
    e.append(e1)
    e.append(e2)
    return e


def multiset_to_tree(multiset):
    """
    :param multiset: A set that can have members FormulaSet, set of FormulaSet and so on.
    :return: An XML 'Sets' tag of the multiset.
    """
    sets = eTree.Element('Sets')

    for fset in multiset:
        if isinstance(fset, FormulaSet):
            set_tag = eTree.Element('Set')

            for formula in fset.formulae:
                f_tag = eTree.Element('Element')
                f_tag.append(formula_to_xml(formula))
                set_tag.append(f_tag)

            sets.append(set_tag)

        else:
            sets.append(multiset_to_tree(fset))

    return sets


def fset_to_tree(fset):
    x_set = eTree.Element('Set')

    for formula in fset.formulae:
        f_tag = eTree.Element('Element')
        f_tag.append(formula_to_xml(formula))
        x_set.append(f_tag)

    return x_set


#TODO figure out what the indent should be so the XML is exactly like that of org_output.xml given.
def writer(xml_element, outfile):
    """
    Writes a properly formatted XML from the given tag.
    :param xml_element: An XML element.
    :param outfile: The file to which the sets is to be written.
    """
    s = eTree.tostring(xml_element)
    outfile = open(outfile, 'w')
    pretty_s = minidom.parseString(s).toprettyxml(indent='\t')
    outfile.write(pretty_s)
    outfile.close()


########################################################################################################################


def TableauRuleApplication(fset):
    """
    Does ONE step of tableaux application.
    That is, looks at the fset.fomulae, and applies a tableaux rule to the first one it can, and returns.
    Also returns whether any rule has been applied (to determine when a tableaux construction is complete)

    Returns a multiset if a rule has been applied.
    Returns the string 'Unmodified' if no rule applied
    (i.e., the given FormulaSet consisted entirely of literals or negation of literals)
    :param fset: A FormulaSet object.
    """

    assert isinstance(fset, FormulaSet)
    multiset = set()

    for formula in fset.formulae:
        if isinstance(formula, Literal):
            pass

        elif isinstance(formula, Negation):

            if isinstance(formula.a, Literal):
                pass

            #Rule 1b
            elif isinstance(formula.a, Negation):
                fset.replace(formula, formula.a.a)
                multiset.add(fset)
                return multiset

            #Rule 2b
            elif isinstance(formula.a, And):
                new1 = Negation(formula.a.a)
                new2 = Negation(formula.a.b)

                fset1, fset2 = fset.split_add(formula, new1, new2)
                multiset.add(fset1)
                multiset.add(fset2)
                return multiset

            #Rule 3b
            elif isinstance(formula.a, Or):
                new1 = Negation(formula.a.a)
                new2 = Negation(formula.a.b)

                fset.replace(formula, new1)
                fset.add(new2)

                multiset.add(fset)
                return multiset

            #Rule 4b
            elif isinstance(formula.a, Implies):
                new1 = formula.a.a
                new2 = Negation(formula.a.b)

                fset.replace(formula, new1)
                fset.add(new2)

                multiset.add(fset)
                return multiset

            #Rule 5b
            elif isinstance(formula.a, DoubleImplies):
                new1 = And(formula.a.a, Negation(formula.a.b))
                new2 = And(Negation(formula.a.a), formula.a.b)

                fset1, fset2 = fset.split_add(formula, new1, new2)
                multiset.add(fset1)
                multiset.add(fset2)
                return multiset

            else:
                raise InvalidFormula

        #Rule 2a
        elif isinstance(formula, And):
            new1 = formula.a
            new2 = formula.b

            fset.replace(formula, new1)
            fset.add(new2)

            multiset.add(fset)
            return multiset

        #Rule 3a
        elif isinstance(formula, Or):
            new1 = formula.a
            new2 = formula.b

            fset1, fset2 = fset.split_add(formula, new1, new2)
            multiset.add(fset1)
            multiset.add(fset2)
            return multiset

        #Rule 4a
        elif isinstance(formula, Implies):
            new1 = Negation(formula.a)
            new2 = formula.b

            fset1, fset2 = fset.split_add(formula, new1, new2)
            multiset.add(fset1)
            multiset.add(fset2)
            return multiset

        #Rule 5a
        elif isinstance(formula, DoubleImplies):
            new1 = And(formula.a, formula.b)
            new2 = And(Negation(formula.a), Negation(formula.b))

            fset1, fset2 = fset.split_add(formula, new1, new2)
            multiset.add(fset1)
            multiset.add(fset2)
            return multiset

        else:
            raise InvalidFormula

    return 'Unmodified'


#TODO if a path contains contradiction (x and ~x), should I stop it right then, or keep extending and branching it.
# TODO add logical equivalence checking.
# Answer : preferably do that shit.
def AnalyticTableaux(fset):
    """
    Takes a FormulaSet and generates an Analytic Tableau for it.
    The tableau takes the form of a multiset. Each Formulaset in the multiset represents a possible path.
    Initiated by calling with a FormulaSet.
    :param fset: A FormulaSet
    """

    tableau = set()
    fset = remove_equivalent(fset)
    tableau.add(fset)
    modified = True
    contradictions = set()

    while modified:
        modified_flag = False

        for cand in tableau:
            applied = TableauRuleApplication(FormulaSet(cand.formulae))
            if applied == 'Unmodified':
                pass
            else:
                tableau.remove(cand)
                for path in applied:
                    if contradiction(path):
                        contradictions.add(path)
                    else:
                        tableau.add(path)
                modified_flag = True
                break

        modified = modified_flag

    return tableau.union(contradictions)


def satisfy(fset):
    tableau = AnalyticTableaux(fset)

    # print(tableau)

    for cand in tableau:
        # print(cand)
        if contradiction(cand):
            pass
        else:
            return True, cand

    return False, tableau


# def contradiction(fset):
#     assert isinstance(fset, FormulaSet)
#     table = {}
#
#     for cand in fset.formulae:
#         if isinstance(cand, Literal):
#             if cand.name in table:
#                 if table[cand.name]:
#                     pass
#                 else:
#                     return True
#
#             else:
#                 table[cand.name] = True
#
#         elif isinstance(cand, Negation):
#             assert isinstance(cand.a, Literal)
#             if cand.a.name in table:
#                 if not table[cand.a.name]:
#                     pass
#                 else:
#                     return True
#
#             else:
#                 table[cand.a.name] = False
#
#     return False

def contradiction(fset):
    assert isinstance(fset, FormulaSet)
    table = {}

    for cand in fset.formulae:
        if not isinstance(cand, Negation):
            if str(cand) in table:
                if table[str(cand)]:
                    pass
                else:
                    return True

            else:
                table[str(cand)] = True

        elif isinstance(cand, Negation):
            # assert isinstance(cand.a, Literal)
            if str(cand.a) in table:
                if not table[str(cand.a)]:
                    pass
                else:
                    return True

            else:
                table[str(cand.a)] = False

    return False


########################################################################################################################


def equivalent(formula1, formula2):
    varlist = sorted(list(set(formula1.vars())))

    if sorted(list(set(formula2.vars()))) != varlist:
        return False

    possibilities = list(product([True, False], repeat=len(varlist)))

    for possibility in possibilities:
        table = {}
        for i in range(0, len(varlist)):
            table[varlist[i]] = possibility[i]

        if formula1.eval(table) == formula2.eval(table):
            pass
        else:
            return False

    return True


def remove_equivalent(fset):
    assert isinstance(fset, FormulaSet)
    formulae = list(fset.formulae)
    unique = []
    for i in range(len(formulae)):
        flag = False
        for j in range(i + 1, len(formulae)):
            # print(i, j)
            if equivalent(formulae[i], formulae[j]):
                flag = True
                break
        if not flag:
            unique += [formulae[i]]

    newset = FormulaSet(unique)
    return newset


def runner(infile, outfile):
    fset = parser(infile)
    satisfiable, proof = satisfy(fset)

    if satisfiable:
        to_write = fset_to_tree(proof)

    else:
        to_write = multiset_to_tree(proof)

    print(satisfiable)
    print(proof)
    writer(to_write, outfile)


runner('input.xml', 'output.xml')

# a = Literal('a')
# b = Literal('b')
# not_b = Negation(b)
# f = And(a, not_b)
# g = And(Or(Literal("x"), Negation(Literal("y"))), f)
#
# myset = FormulaSet([a, b, f, g])
# print(myset)
#
# test_in = parser('test.xml')
#
# print(test_in)
#
# test_tableau = (AnalyticTableaux(test_in))
#
# test_tree = multiset_to_tree(test_tableau)
#
# writer(test_tree, 'test.xml')
#
# a = Literal('a')
# b = Literal('b')
# notb = Negation(b)
# f = And(Or(a, notb), b)
# g = Or(And(a, notb), b)
# fs = FormulaSet([f, g])
# fs.add(a)
# fs.add(Negation(Negation(a)))
# re = remove_equivalent

# a