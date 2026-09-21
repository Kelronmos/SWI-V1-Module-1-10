⚠️ SWI WARNING FOR EXPERIMENTERS

If you experiment with SWI, don't confuse something you can run with something that is sealed.

Named ≠ Implemented  
Implemented ≠ Tested  
Tested ≠ Sealed  
Sealed ≠ Authorized

Current PRE-R work is explicitly EXPERIMENTAL.

It is NOT SEALED.  
Formal promotion is NOT AUTHORIZED.  
PRE-CONSEQUENCES is NOT IMPLEMENTED.

PR-009 demonstrates an enforced experimental API path.

It does not prove process-wide enforcement, structural impossibility of bypass, or production authorization.

If you fork it, modify it, experiment with it, or build on it:

Do not present your experiment as SWI-sealed capability.

Record the exact commit.  
Record what you changed.  
Run the tests.  
Record what passed.  
Record what failed.  
Keep the limitations visible.

And don't silently upgrade the status.

A passing local test does not make something sealed.  
A working demo does not make something authorized.

If stronger guarantees are required, follow the applicable formal promotion and verification process.

This isn't bureaucracy.

It is how we prevent an experiment from quietly becoming a false claim about capability, safety, or readiness.
