# MDP-fish-problem
A calculator for evaluating the Markov Decision Process for a fish business example.

The original Excel macro code was released by Dr. Russel King and was converted by Jack Wilson.

## Problem

A wharf-side fish market sells live fish from its tank during the afternoon. The tank can hold at most 12 fish. During the morning, fish are caught from local waters and used to restock the tank. The number of fish caught, F, has the following mass function.

$$
\begin{equation}
  p_{F}(f)=
  \begin{cases}
    0.1, & f=0 \\
    0.2, & f=1 \\
    0.3, & f=2 \\
    0.2, & f=3 \\
    0.1, & f=4 \\
    0.1, & f=5 
  \end{cases}
\end{equation}
$$

If there is not enough room in the tank for the number of fish caught, then the excess is sold to local restaurants for $12/fish. Consumer demand during any day (D) for live fish has the following probability mass function.

$$
\begin{equation}
  p_{D}(d)=
  \begin{cases}
    0.2, & f=0 \\
    0.2, & f=1 \\
    0.3, & f=2 \\
    0.2, & f=3 \\
    0.1, & f=4 
  \end{cases}
\end{equation}
$$

The cost to catch each fish is about $4.00/fish caught plus a fixed fuel surcharge of $20/day. The selling price out of the tank is $20.00. Assume a Markov model is desired where the state of the system is defined to be the number of fish in the tank at the end of each day.

