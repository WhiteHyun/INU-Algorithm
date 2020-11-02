import time
from init import *
INTERNAL_NODE_VALUE = -1


class RadixSearchTrie(Tree):
    """
    탐색 알고리즘 중 기수 탐색 트라이에 해당하는 클래스입니다.
    Tree를 상속받습니다. Tree에 대한 정보는 Tree.__doc__ 명령어를 사용해주세요.
    """

    def __init__(self, data_size) -> None:
        super().__init__(data_size)

    def insert(self, key: int) -> int:
        """
        기수 탐색 트라이에서 노드를 넣는 함수입니다.

        Args:

            key (int): 노드의 key값을 넣기 위한 파라미터입니다.

        Returns:
            0: Success
            -2: Error
        """
        x: Node = self.head.right  # 비교노드
        p_node: Node = self.head    # 부모노드
        temp_node: Node = Node(key, self.maxb)  # Insert할 임시 노드
        h: int = -1  # 이진수 인덱스
        try:
            # 값이 존재하지 않거나 내부노드인 경우만 반복하여 넣을 공간을 찾아감
            while x is not None and x.key == INTERNAL_NODE_VALUE:
                p_node = x
                if temp_node.binkey[h] == "1":
                    x = x.right
                else:
                    x = x.left
                h -= 1
            # 첫 번째 노드를 넣을 경우
            if h == -1 and x is None:
                p_node.right = temp_node
            # 단독으로 노드를 넣을 경우
            elif x is None:
                if p_node.right == x:
                    p_node.right = temp_node
                else:
                    p_node.left = temp_node
            # 존재하고있는 key값과 경쟁을 하는 경우
            else:
                # 먼저 내부노드를 설정하여 부모노드와 연결한다.
                internal_node = Node(INTERNAL_NODE_VALUE, self.maxb)
                if p_node.right == x:
                    p_node.right = internal_node
                else:
                    p_node.left = internal_node
                p_node = internal_node
                # 기존에 존재하던 노드와 넣을 노드간 비트 비교를 통해 내부노드를 따라 내려갈지 아닐지를 결정한다.
                while x.binkey[h] == temp_node.binkey[h]:
                    internal_node = Node(INTERNAL_NODE_VALUE, self.maxb)
                    if temp_node.binkey[h] == "1":
                        p_node.right = internal_node
                    else:
                        p_node.left = internal_node
                    p_node = internal_node
                    h -= 1
                # 경쟁이 끝났다면 각 비트에 따라 자식노드로 넣어준다
                if temp_node.binkey[h] == "1":
                    p_node.right = temp_node
                    p_node.left = x
                else:
                    p_node.right = x
                    p_node.left = temp_node
        except:
            return ERROR
        return SUCCESS

    def search(self, search_key: int) -> int:
        """
        탐색 함수입니다.

        Args:

            search_key (int): 트리 내에서 탐색할 key 값입니다.

        Returns:
            0: Success
            -1: Search Failed
            -2: Search Error
        """
        # 탐색키의 5자리 이진수 문자열
        bin_search_key: str = self.head.key_to_bin(search_key)
        x: Node = self.head.right   # 탐색노드
        p_node: Node = self.head  # 탐색노드의 부모노드
        h: int = 0  # 이진수 인덱스 내지는 트리 높이를 가리킴
        try:
            # 내부 노드를 벗어날 때까지 이동
            while x.key == INTERNAL_NODE_VALUE:
                p_node = x
                if bin_search_key[h] == "1":
                    x = x.right
                else:
                    x = x.left
                h += 1
            if x.key == search_key:
                return x.key
        except:
            return ERROR
        return FAIL

    def check(self, key_list: list, time: float) -> None:
        print("=================================================================")
        print(key_list)
        for key in sorted(key_list):
            print(key, end=" ")
            p = x = self.head.right
            bin_key = self.head.key_to_bin(key)[::-1]
            for i in range(len(bin_key)-1, -2, -1):
                if x.key == key:
                    print()
                    break
                p = x
                if bin_key[i] == "1":
                    x = x.right
                    print("right", end=" ")
                else:
                    x = x.left
                    print("left", end=" ")

        print(f"""기수 탐색 트라이의 실행 시간 (N = {len(key_list)}: {time:.3f})
탐색 완료
=================================================================""")


if __name__ == "__main__":
    d = RadixSearchTrie(26)
    keys = [1, 19, 5, 18, 3, 26, 9]
    for i in keys:
        result = d.insert(i)
        if result == -2:
            print(f'오류! key = {i}')
    start_time = time.time()
    for i in keys:
        result = d.search(i)
        # if result == -2:
        #     print("탐색오류발생")
        # elif result == -1:
        #     print("탐색실패")
        # else:
        #     print(f"탐색성공, key = {result}")
    end_time = time.time() - start_time
    d.check(keys, end_time)

# if __name__ == "__main__":
#     data = 30000
#     d = RadixSearchTrie(data)
#     keys = list(range(1, data+1))
#     for i in keys:
#         d.insert(i)
#     start_time = time.time()
#     for i in keys:
#         if d.search(i) != i:
#             print("error")
#     end_time = time.time() - start_time
#     print(f'내 기수 탐색 트라이 코드(N= {data}) : {end_time:.3f}')
