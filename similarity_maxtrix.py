class matrix:

    def __init__(self):
        self.Similarity_matrix_edge = {'Association': {}, 'composite': {}, 'AttributeEdge': {}, 'generalization': {},
                                       'interfaceRealization': {}, 'shared': {}}
        self.Similarity_matrix_edge['Association']['Association'] = 1
        self.Similarity_matrix_edge['Association']['composite'] = 0.89
        self.Similarity_matrix_edge['Association']['AttributeEdge'] = 0.25
        self.Similarity_matrix_edge['Association']['generalization'] = 0.55
        self.Similarity_matrix_edge['Association']['interfaceRealization'] = 0.23
        self.Similarity_matrix_edge['Association']['shared'] = 0.89

        self.Similarity_matrix_edge['composite']['composite'] = 1
        self.Similarity_matrix_edge['composite']['Association'] = 0.89
        self.Similarity_matrix_edge['composite']['AttributeEdge'] = 0.1
        self.Similarity_matrix_edge['composite']['generalization'] = 0.55
        self.Similarity_matrix_edge['composite']['interfaceRealization'] = 0.23
        self.Similarity_matrix_edge['composite']['shared'] = 0.89

        self.Similarity_matrix_edge['AttributeEdge']['AttributeEdge'] = 1
        self.Similarity_matrix_edge['AttributeEdge']['Association'] = 0.25
        self.Similarity_matrix_edge['AttributeEdge']['composite'] = 0.1
        self.Similarity_matrix_edge['AttributeEdge']['generalization'] = 0.75
        self.Similarity_matrix_edge['AttributeEdge']['interfaceRealization'] = 0.1
        self.Similarity_matrix_edge['AttributeEdge']['shared'] = 0.25

        self.Similarity_matrix_edge['generalization']['generalization'] = 1
        self.Similarity_matrix_edge['generalization']['Association'] = 0.51
        self.Similarity_matrix_edge['generalization']['composite'] = 0.51
        self.Similarity_matrix_edge['generalization']['AttributeEdge'] = 0.75
        self.Similarity_matrix_edge['generalization']['interfaceRealization'] = 0.4
        self.Similarity_matrix_edge['generalization']['shared'] = 0.51

        self.Similarity_matrix_edge['interfaceRealization']['AttributeEdge'] = 0.1
        self.Similarity_matrix_edge['interfaceRealization']['Association'] = 0
        self.Similarity_matrix_edge['interfaceRealization']['composite'] = 0
        self.Similarity_matrix_edge['interfaceRealization']['generalization'] = 0.21
        self.Similarity_matrix_edge['interfaceRealization']['interfaceRealization'] = 1
        self.Similarity_matrix_edge['interfaceRealization']['shared'] = 0

        self.Similarity_matrix_edge['shared']['shared'] = 1
        self.Similarity_matrix_edge['shared']['Association'] = 0.89
        self.Similarity_matrix_edge['shared']['composite'] = 0.89
        self.Similarity_matrix_edge['shared']['AttributeEdge'] = 0.25
        self.Similarity_matrix_edge['shared']['generalization'] = 0.55
        self.Similarity_matrix_edge['shared']['interfaceRealization'] = 0.23

        self.Similarity_matrix_class = {'Class': {}, 'Abstract': {}, 'Interface': {}, 'Attribute': {},
                                        'AssociationClass': {}}

        self.Similarity_matrix_class['Class']['Class'] = 1
        self.Similarity_matrix_class['Class']['Abstract'] = 0.75
        self.Similarity_matrix_class['Class']['Interface'] = 0.4
        self.Similarity_matrix_class['Class']['Attribute'] = 0.1
        self.Similarity_matrix_class['Class']['AssociationClass'] = 0.8

        self.Similarity_matrix_class['Abstract']['Class'] = 0.75
        self.Similarity_matrix_class['Abstract']['Abstract'] = 1
        self.Similarity_matrix_class['Abstract']['Interface'] = 0.75
        self.Similarity_matrix_class['Abstract']['Attribute'] = 0.1
        self.Similarity_matrix_class['Abstract']['AssociationClass'] = 0.7

        self.Similarity_matrix_class['Interface']['Class'] = 0.4
        self.Similarity_matrix_class['Interface']['Abstract'] = 0.7
        self.Similarity_matrix_class['Interface']['Interface'] = 1
        self.Similarity_matrix_class['Interface']['Attribute'] = 0.05
        self.Similarity_matrix_class['Interface']['AssociationClass'] = 0.2

        self.Similarity_matrix_class['Attribute']['Class'] = 0.1
        self.Similarity_matrix_class['Attribute']['Abstract'] = 0.1
        self.Similarity_matrix_class['Attribute']['Interface'] = 0.05
        self.Similarity_matrix_class['Attribute']['Attribute'] = 1
        self.Similarity_matrix_class['Attribute']['AssociationClass'] = 0.05

        self.Similarity_matrix_class['AssociationClass']['AssociationClass'] = 1
        self.Similarity_matrix_class['AssociationClass']['Class'] = 0.6
        self.Similarity_matrix_class['AssociationClass']['Abstract'] = 0.7
        self.Similarity_matrix_class['AssociationClass']['Interface'] = 0
        self.Similarity_matrix_class['AssociationClass']['Attribute'] = 0.05

    def edge_matrix(self):
        return self.Similarity_matrix_edge

    def class_matrix(self):
        return self.Similarity_matrix_class
