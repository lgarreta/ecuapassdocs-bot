package results;

import java.awt.Component;
import java.awt.Container;
import java.awt.FocusTraversalPolicy;
import java.util.ArrayList;

//-------------------------------------------------------------------
// Class for assigning focus according to components creation
//-------------------------------------------------------------------
public class CustomFocusTraversalPolicy extends FocusTraversalPolicy {

	private final ArrayList<Component> order;

	public CustomFocusTraversalPolicy (Component[] order) {
		this.order = new ArrayList<> ();
		for (Component component : order) {
			this.order.add (component);
		}
	}

	@Override
	public Component getComponentAfter (Container container, Component component) {
		int index = order.indexOf (component);
		if (index < order.size () - 1)
			return order.get (index + 1);
		else
			return order.get (0);
	}

	@Override
	public Component getComponentBefore (Container container, Component component) {
		int index = order.indexOf (component);
		if (index > 0)
			return order.get (index - 1);
		else
			return order.get (order.size () - 1);
	}

	@Override
	public Component getFirstComponent (Container container) {
		return order.get (0);
	}

	@Override
	public Component getLastComponent (Container container) {
		return order.get (order.size () - 1);
	}

	@Override
	public Component getDefaultComponent (Container container) {
		return getFirstComponent (container);
	}
}

