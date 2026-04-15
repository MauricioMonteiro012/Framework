class ProductDomain:
    def __init__(self, id, nome, preco, qtd, status, img, user_id):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.qtd = qtd
        self.status = status
        self.img = img
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "qtd": self.qtd,
            "status": self.status,
            "img": self.img,
            "user_id": self.user_id
        }                                   