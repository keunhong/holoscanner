using UnityEngine;
using System.Collections;

namespace DeerCat
{

	public class DemoController : MonoBehaviour
	{
		private int activeIndex = 0;
		private int numItems = 0;

		private UnityEngine.UI.Text itemNameUI;
		private GameObject activeItem;

		void Start()
		{
			numItems = transform.childCount;
			itemNameUI = GameObject.Find("ItemName").GetComponent<UnityEngine.UI.Text>();

			// make all particle systems loop for the demo
			ParticleSystem[] ps = GetComponentsInChildren<ParticleSystem>();
			for (int i = 0; i < ps.Length; ++i)
				ps[i].loop = true;

			for (int i = 0; i < numItems; ++i)
			{
				GameObject item = transform.GetChild(i).gameObject;
				item.SetActive(false);
			}

			ActivateCurrentItem();
		}

		void Update()
		{
			if (Input.GetKeyUp(KeyCode.RightArrow))
				NextItem();
			else if (Input.GetKeyUp(KeyCode.LeftArrow))
				PrevItem();
		}

		private void ActivateCurrentItem()
		{
			if (activeItem != null)
				activeItem.SetActive(false);

			activeItem = transform.GetChild(activeIndex).gameObject;
			activeItem.SetActive(true);
			itemNameUI.text = activeItem.name;
		}

		public void NextItem()
		{
			activeIndex = (activeIndex + 1) % numItems;
			ActivateCurrentItem();
		}

		public void PrevItem()
		{
			activeIndex = activeIndex == 0 ? numItems - 1 : activeIndex - 1;
			ActivateCurrentItem();
		}
	}

}
