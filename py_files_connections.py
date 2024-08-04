import os
import re
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

def find_python_files(directory):
    """Поиск всех файлов с расширением .py в указанной директории, исключая .venv."""
    python_files = []
    for root, _, files in os.walk(directory):
        if '.venv' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports(file_path):
    """Извлчение строк import и from из файла .py."""
    imports = set()
    import_pattern = re.compile(r'^\s*(import|from)\s+([a-zA-Z0-9_\.]+)')
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = import_pattern.match(line)
            if match:
                imports.add(match.group(2))
    return imports

def get_file_name(file_path):
    """Извлчение имени файла из полного пути."""
    return os.path.basename(file_path)

def build_import_map(directory):
    """Создание карты импортов для всех файлов .py в указанной директории."""
    import_map = defaultdict(set)
    python_files = find_python_files(directory)
    for file_path in python_files:
        imports = extract_imports(file_path)
        file_name = get_file_name(file_path)
        import_map[file_name].update(imports)
    return import_map

def build_dependency_graph(import_map):
    """Создание графа зависимостей между файлами на основе карты импортов."""
    dependency_graph = defaultdict(set)
    for file_name, imports in import_map.items():
        for imported_module in imports:
            for other_file_name, other_imports in import_map.items():
                if other_file_name != file_name and imported_module in other_imports:
                    dependency_graph[file_name].add(other_file_name)
    return dependency_graph

def visualize_dependency_graph(dependency_graph):
    """Визуализация графа зависимостей с использованием networkx и matplotlib."""
    G = nx.DiGraph()

    for file, dependencies in dependency_graph.items():
        for dependency in dependencies:
            G.add_edge(file, dependency)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrowsize=20)
    plt.title('Dependency Graph')
    plt.show()

def main():
    directory = 'C:\\PycharmProjects\\SM'  # Путь к проекту (указать исследуемую директорию)
    import_map = build_import_map(directory)
    dependency_graph = build_dependency_graph(import_map)

    print("Import Map:")
    for file, imports in import_map.items():
        print(f"{file}: {', '.join(imports)}")

    print("\nDependency Graph:")
    for file, dependencies in dependency_graph.items():
        print(f"{file} depends on {', '.join(dependencies)}")

    visualize_dependency_graph(dependency_graph)

if __name__ == "__main__":
    main()
