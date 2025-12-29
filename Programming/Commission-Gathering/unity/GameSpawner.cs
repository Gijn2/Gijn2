using UnityEngine;

public class GameSpawner : MonoBehaviour
{
    public GameObject[] characterPrefabs; // 캐릭터 모델들을 담아두는 리스트
    public Transform spawnPoint; // 소환될 위치

    void Start()
    {
        int index = CharacterManager.instance.selectedCharacterIndex;
        Instantiate(characterPrefabs[index], spawnPoint.position, Quaternion.identity);
    }
}