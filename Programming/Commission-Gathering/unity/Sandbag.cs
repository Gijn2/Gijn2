using UnityEngine;

public class Sandbag : MonoBehaviour
{
    public int hp = 100;

    void OnCollisionEnter(Collision collision)
    {
        if (collision.gameObject.CompareTag("Skill")) // 스킬에 맞으면
        {
            hp -= 10;
            Debug.Log("샌드백 체력: " + hp);
            Destroy(collision.gameObject); // 투사체 삭제
            
            // 여기서 샌드백 흔들림 애니메이션 등을 실행할 수 있습니다.
        }
    }
}