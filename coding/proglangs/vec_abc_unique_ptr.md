# vector of abstract-base-class unique_ptr as data member

Smart pointers have been available since C++11. For developers, it is always a good question whether to use `unique_ptr` or `shared_ptr`. As a rule of thumb, unless you have to use shared_ptr, **use `unique_ptr`**. Further, **use `make_unique` to create unique_ptr instance**, if possible.

Unfortunately, unique_ptr can be hard to use because it cannot be copied or assigned. This may lead to compiling errors that point to the standard library headers and are difficult to decipher (or debug).

To make the points easy to see, I will go over the details of using a `vector` of unique_ptr's of *abstract base class* (ABC) as a *data member* below.

The ABC and derived classes are defined in BaseAndDerived.h:
```
#include <iostream>

using namespace std;

struct IFaceQL {		// ABC
	virtual ~IFaceQL() = default;	
	virtual void use() = 0;
	virtual bool isAlive() const { return false; }
};

struct DerivedA : public IFaceQL {
	void use() override {cout << "use DerivedA\n";}
	bool isAlive() const { return true; }
};

struct DerivedB : public IFaceQL {
	void use() override {cout << "use DerivedB: " << mName << endl;}
	bool isAlive() const { return mName.empty()? false: true; }

	DerivedB(const string & name_in): mName(name_in) {}
	string mName{};
	~DerivedB() { cout << mName << " ~DerivedB() called\n\n"; }
};
```

The use case and test are in smartPtrVecDM.cpp:
```
#include "BaseAndDerived.h"

#include <memory>
#include <vector>

using namespace std;

// class with vector of unique_ptr of ABC as DM
class PtrVecDataMem {	
	int mDummy;
	vector< unique_ptr< IFaceQL> > mUniqVec;

public:
	PtrVecDataMem(int x): mDummy(x) {}
	
	void initUniqueVector() {	
		// puch_back: not member
		//mUniqVec.puch_back(make_unique<DerivedA>());

		mUniqVec.emplace_back(make_unique<DerivedB>("B-1"));	// OK
		mUniqVec.emplace_back(make_unique<DerivedA>());		// OK

		// error C2672: 'std::construct_at': no matching overloaded function found
		//auto pA = make_unique<DerivedA>();
		//mUniqVec.emplace_back(pA);

		auto pB = make_unique<DerivedB>("");
		if (pB->isAlive()) mUniqVec.emplace_back(move(pB));	//OK: move
		auto pB2 = make_unique<DerivedB>("B-2");
		if (pB2->isAlive()) mUniqVec.emplace_back(move(pB2));

		cout << "\ninitUniqueVector()---\n";
		for (auto& ptr : mUniqVec) ptr->use();
	}
};


int main() {
	PtrVecDataMem me{ 27 };
	me.initUniqueVector();

	cout << "\nmain()---\n";
	return 0;
}
```
You can read the comments in the code for all you need to know. Briefly:
1. Visual Studio 2026 (vs2026) will indicate that `puch_back` is not a member and thus cannot be used;
2. `emplace_back` with `make_unique` as an argument works;
3. Passing a named instance (*lvalue*) to `emplace_back`, you get error C2672: 
> 'std::construct_at': no matching overloaded function found

which points to *xmemory* and does not make too much sense for debugging:

![error C2672](images/error_C2672.png)

If you review *Output* in the vs2026 IDE, you can find something like this:

> cannot convert argument 1 from 'std::unique_ptr<DerivedA,std::default_delete<DerivedA>>' to 'std::unique_ptr<DerivedA,std::default_delete<DerivedA>> &&'

The double `&&` at the end means *rvalue*, which can be achieved by `std::move`.

4. `emplace_back` with `std::move` as an argument works.