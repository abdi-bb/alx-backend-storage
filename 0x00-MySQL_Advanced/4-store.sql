-- AFTER INSERT trigger
-- Create a trigger to decrease the quantity of items after adding an order
DROP TRIGGER IF EXISTS decrease_quantity_after_order;
DELIMITER $$
CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW 
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END
$$
DELIMITER ;