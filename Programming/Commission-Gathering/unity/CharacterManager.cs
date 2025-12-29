using UnityEngine;
using UnityEngine.SceneManagement;

public class CharacterManager : MonoBehaviour
{
    public static CharacterManager instance;
    public int selectedCharacterIndex; // 선택된 캐릭터 번호

    void Awake()
    {
        if (instance == null) {
            instance = this;
            DontDestroyOnLoad(gameObject); // 씬이 넘어가도 삭제되지 않음
        } else {
            Destroy(gameObject);
        }
    }

    public void SelectCharacter(int index)
    {
        selectedCharacterIndex = index;
        SceneManager.LoadScene("InGame"); // 인게임 씬으로 이동
    }
}