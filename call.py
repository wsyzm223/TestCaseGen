from test_data_gen_class import TestDataGenerator
from config import DEFAULT_CONFIG

my_config = {
    "max_age": 60,
    "min_age": 20,
    "domains": ["futu.com", "futunn.com"],
    "age_if_include_boundary": True,
    "age_boundary_offsets": [-0.5, -1, 0, 1, 0.5],
}
test_data_1 = TestDataGenerator(DEFAULT_CONFIG)
test_data_2 = TestDataGenerator(my_config)
print(TestDataGenerator.count)