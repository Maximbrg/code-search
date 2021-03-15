class matrix:

    def __init__(self):
        self.Similarity_matrix_edge = {}
        self.Similarity_matrix_edge['achieved by'] = {}
        self.Similarity_matrix_edge['achieved by']['achieved by'] = 1
        self.Similarity_matrix_edge['achieved by']['consists of'] = 0.5
        self.Similarity_matrix_edge['achieved by'][''] = 0.25
        self.Similarity_matrix_edge['achieved by']['+'] = 0.25
        self.Similarity_matrix_edge['achieved by']['++'] = 0.25
        self.Similarity_matrix_edge['achieved by']['--'] = 0.25
        self.Similarity_matrix_edge['achieved by']['-'] = 0.25

        self.Similarity_matrix_edge['consists of'] = {}
        self.Similarity_matrix_edge['consists of']['consists of'] = 1
        self.Similarity_matrix_edge['consists of'][''] = 0.25
        self.Similarity_matrix_edge['consists of']['+'] = 0.25
        self.Similarity_matrix_edge['consists of']['++'] = 0.25
        self.Similarity_matrix_edge['consists of']['-'] = 0.25
        self.Similarity_matrix_edge['consists of']['--'] = 0.25

        self.Similarity_matrix_edge[''] = {}
        self.Similarity_matrix_edge[''][''] = 1
        self.Similarity_matrix_edge['']['+'] = 0.25
        self.Similarity_matrix_edge['']['++'] = 0.25
        self.Similarity_matrix_edge['']['-'] = 0.25
        self.Similarity_matrix_edge['']['--'] = 0.25

        self.Similarity_matrix_edge['+'] = {}
        self.Similarity_matrix_edge['+']['+'] = 1
        self.Similarity_matrix_edge['+']['++'] = 0.8
        self.Similarity_matrix_edge['+']['-'] = 0
        self.Similarity_matrix_edge['+']['--'] = 0

        self.Similarity_matrix_edge['++'] = {}
        self.Similarity_matrix_edge['++']['++'] = 1
        self.Similarity_matrix_edge['++']['-'] = 0
        self.Similarity_matrix_edge['++']['--'] = 0

        self.Similarity_matrix_edge['-'] = {}
        self.Similarity_matrix_edge['-']['-'] = 1
        self.Similarity_matrix_edge['-']['--'] = 0.8

        self.Similarity_matrix_edge['--'] = {}
        self.Similarity_matrix_edge['--']['--'] = 1

        self.Similarity_matrix_class = {'Task': {}, 'Quality': {}}

        self.Similarity_matrix_class['Quality']['Quality'] = 1
        self.Similarity_matrix_class['Task']['Task'] = 1
        self.Similarity_matrix_class['Task']['Quality'] = 0.5
        self.Similarity_matrix_class['Quality']['Task'] = 0.5


    def edge_matrix(self):
        return self.Similarity_matrix_edge

    def class_matrix(self):
        return self.Similarity_matrix_class
