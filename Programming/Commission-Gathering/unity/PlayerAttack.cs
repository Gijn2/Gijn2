using UnityEngine;

public class PlayerAttack : MonoBehaviour
{
    public GameObject projectilePrefab; // 스킬 이펙트/투사체
    public Transform firePoint;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Q))
        {
            Attack();
        }
    }

    void Attack()
    {
        // 마우스 방향 계산
        Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
        if (Physics.Raycast(ray, out RaycastHit hit))
        {
            Vector3 targetDir = (hit.point - transform.position).normalized;
            targetDir.y = 0; // 바닥 평면으로 방향 고정

            // 투사체 생성 및 발사
            GameObject bullet = Instantiate(projectilePrefab, firePoint.position, Quaternion.LookRotation(targetDir));
            bullet.GetComponent<Rigidbody>().velocity = targetDir * 20f; // 초속 20으로 발사
        }
    }
}