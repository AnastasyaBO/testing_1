from testing_1.Calculat.app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calculate_correctly(self):#позитивное тестирование умножения
        assert self.calc.multiply(self, 2, 2) == 4

    def test_multiply_calculate_faild(self):#негативное тестирование умножения
        assert self.calc.multiply(self, 2, 2) == 5

    def test_division_calculate_correctly(self):#позитивное тестирование деление
        assert self.calc.division(self, 4, 2) == 2

    def test_division_calculate_faild(self):#негативное тестирование деление
        assert self.calc.division(self, 4, 2) == 3

    def test_subtraction_calculate_correctly(self):#позитивное тестирование вычетание
        assert self.calc.subtraction(self, 5, 2) == 3

    def test_subtraction_calculate_faild(self):#негативное тестирование вычетание
        assert self.calc.subtraction(self, 5, 2) == 1

    def test_adding_calculate_correctly(self):#позитивное тестирование сложение
        assert self.calc.adding(self, 5, 2) == 7

    def test_adding_calculate_faild(self):#негативное тестирование сложение
        assert self.calc.adding(self, 5, 2) == 5