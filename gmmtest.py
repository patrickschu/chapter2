import sklearn
from sklearn import datasets
from sklearn import mixture
#import clustertools as ct

iris = datasets.load_iris()
print iris.target



#model=sklearn.mixture.GMM(n_components=3, covariance_type='diag', init_params='wc', n_iter=20)

# model.fit(iris.data)
# 
# print model.predict(iris.data)


for x in [2,4,6,8,12,16,20,24]:
	model=sklearn.mixture.GMM(x, n_iter=100, verbose=0)
	model.fit(iris.data)
	print "\n predict", model.predict(iris.data)
	print "means", model.means_
	print "\n predict probs", model.predict_proba(iris.data)
	#dirichlet= ct.Clustering(model, model.predict(iris.data), model.means_)


print iris.data