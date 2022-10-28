/** translation of point2.py */

import java.lang.Math;

/** translation of point2.py with verbose comments */
public class Point  // public so available to all other classes
{
    private double x, y; // instance variable, private, NOT in a method

    public Point(double x, double y)
    // constructor: method with class name, no return value
    {
        this.x = x;   // this in place of Python self
        this.y = y;
    }

    public double getX()
    {
        return x; // no this: no need to disambiguate x
    }        // If a variable is not local, next check instance variables

    public double getY()
    {
        return y;
    }

    public double distanceFromOrigin()
    {
        return Math.sqrt(x*x + y*y);  // no ** operator
    }

    /** return vector difference. this - pt */
    public Point diff(Point pt)  // cannot overload "-" operator
    {
        return new Point(x - pt.x, y - pt.y);  // note required "new"
        // for other Point, pt, must use dot notation
    }

    /** return distance between this and pt */
    public double distance(Point pt)
    {
        return diff(pt).distanceFromOrigin(); // not need this. with diff
    }

    /** return Point halfway between this Point and target */
    public Point halfway(Point target)
    {
        double mx = (x + target.x)/2;  // target needs dot notation while
        double my = (y + target.y)/2;  //   instance variables for this do not
        return new Point(mx, my);      // again note "new"
    }

    public String toString()
    {
        return String.format("x = %f, y = %f", x, y);
    }
}